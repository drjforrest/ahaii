#!/usr/bin/env python3
"""
AHAII ETL Scheduler System
Production-ready scheduler for automated ETL pipeline execution with monitoring and alerting
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import schedule
import time

from loguru import logger

from .orchestrator import AHAIIETLOrchestrator, PipelineStatus
from .data_quality_manager import AHAIIDataQualityManager
from services.database_service import DatabaseService
from config.database import supabase


class ScheduleType(Enum):
    """Types of scheduled tasks"""

    CRON = "cron"
    INTERVAL = "interval"
    ONE_TIME = "one_time"


@dataclass
class ScheduledTask:
    """Represents a scheduled ETL task"""

    task_id: str
    name: str
    description: str
    schedule_type: ScheduleType
    schedule_expression: str  # Cron expression or interval
    pipeline_function: Callable
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    failure_count: int = 0
    max_failures: int = 3
    timeout_minutes: int = 120
    retry_delay_minutes: int = 15

    # Notification settings
    notify_on_success: bool = False
    notify_on_failure: bool = True
    notification_emails: List[str] = None

    # Metadata
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.notification_emails is None:
            self.notification_emails = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


class AHAIIETLScheduler:
    """Production ETL scheduler with monitoring and alerting"""

    def __init__(self):
        self.orchestrator = AHAIIETLOrchestrator()
        self.quality_manager = AHAIIDataQualityManager()
        self.db_service = DatabaseService()

        # Task storage
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}

        # Scheduler state
        self.is_running = False
        self.startup_time = datetime.now()

        # Configure default scheduled tasks
        self._setup_default_schedule()

    def _setup_default_schedule(self):
        """Setup default ETL pipeline schedules"""

        # News Monitoring - Every 6 hours
        self.add_scheduled_task(
            ScheduledTask(
                task_id="news_monitoring_6h",
                name="News Monitoring Pipeline",
                description="Monitor health AI infrastructure news from RSS feeds",
                schedule_type=ScheduleType.INTERVAL,
                schedule_expression="6h",
                pipeline_function=self._run_news_monitoring,
                timeout_minutes=30,
                notify_on_failure=True,
                notification_emails=["admin@ahaii.org"],
            )
        )

        # Academic Processing - Daily at 2 AM
        self.add_scheduled_task(
            ScheduledTask(
                task_id="academic_processing_daily",
                name="Academic Processing Pipeline",
                description="Process academic papers and extract infrastructure indicators",
                schedule_type=ScheduleType.CRON,
                schedule_expression="0 2 * * *",  # Daily at 2 AM
                pipeline_function=self._run_academic_processing,
                timeout_minutes=120,
                notify_on_failure=True,
                notification_emails=["admin@ahaii.org"],
            )
        )

        # AHAII Scoring - Twice daily at 6 AM and 6 PM
        self.add_scheduled_task(
            ScheduledTask(
                task_id="scoring_twice_daily",
                name="AHAII Scoring Pipeline",
                description="Calculate and update AHAII scores based on latest data",
                schedule_type=ScheduleType.CRON,
                schedule_expression="0 6,18 * * *",  # 6 AM and 6 PM daily
                pipeline_function=self._run_scoring,
                timeout_minutes=60,
                notify_on_failure=True,
                notification_emails=["admin@ahaii.org"],
            )
        )

        # Data Quality Check - Every 4 hours
        self.add_scheduled_task(
            ScheduledTask(
                task_id="data_quality_4h",
                name="Data Quality Check",
                description="Validate data quality and identify issues",
                schedule_type=ScheduleType.INTERVAL,
                schedule_expression="4h",
                pipeline_function=self._run_data_quality_check,
                timeout_minutes=15,
                notify_on_failure=True,
                notification_emails=["admin@ahaii.org"],
            )
        )

        # Full Pipeline - Weekly on Sunday at 1 AM
        self.add_scheduled_task(
            ScheduledTask(
                task_id="full_pipeline_weekly",
                name="Complete ETL Pipeline",
                description="Execute complete ETL pipeline with all components",
                schedule_type=ScheduleType.CRON,
                schedule_expression="0 1 * * 0",  # Sunday at 1 AM
                pipeline_function=self._run_full_pipeline,
                timeout_minutes=180,
                notify_on_success=True,
                notify_on_failure=True,
                notification_emails=["admin@ahaii.org"],
            )
        )

    def add_scheduled_task(self, task: ScheduledTask) -> bool:
        """Add a new scheduled task"""
        try:
            # Validate schedule expression
            if not self._validate_schedule_expression(
                task.schedule_type, task.schedule_expression
            ):
                logger.error(f"Invalid schedule expression: {task.schedule_expression}")
                return False

            # Calculate next run time
            task.next_run = self._calculate_next_run(
                task.schedule_type, task.schedule_expression
            )

            self.scheduled_tasks[task.task_id] = task
            logger.info(
                f"📅 Added scheduled task: {task.name} ({task.schedule_expression})"
            )
            logger.info(f"   Next run: {task.next_run}")

            return True

        except Exception as e:
            logger.error(f"Failed to add scheduled task {task.name}: {e}")
            return False

    def remove_scheduled_task(self, task_id: str) -> bool:
        """Remove a scheduled task"""
        try:
            if task_id in self.scheduled_tasks:
                task = self.scheduled_tasks.pop(task_id)
                logger.info(f"🗑️ Removed scheduled task: {task.name}")

                # Cancel if currently running
                if task_id in self.running_tasks:
                    self.running_tasks[task_id].cancel()
                    del self.running_tasks[task_id]

                return True
            else:
                logger.warning(f"Task not found: {task_id}")
                return False

        except Exception as e:
            logger.error(f"Failed to remove scheduled task {task_id}: {e}")
            return False

    def enable_task(self, task_id: str) -> bool:
        """Enable a scheduled task"""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id].enabled = True
            self.scheduled_tasks[task_id].updated_at = datetime.now()
            logger.info(f"✅ Enabled task: {self.scheduled_tasks[task_id].name}")
            return True
        return False

    def disable_task(self, task_id: str) -> bool:
        """Disable a scheduled task"""
        if task_id in self.scheduled_tasks:
            self.scheduled_tasks[task_id].enabled = False
            self.scheduled_tasks[task_id].updated_at = datetime.now()
            logger.info(f"❌ Disabled task: {self.scheduled_tasks[task_id].name}")
            return True
        return False

    async def start_scheduler(self):
        """Start the ETL scheduler"""
        logger.info("🚀 Starting AHAII ETL Scheduler...")

        self.is_running = True
        self.startup_time = datetime.now()

        # Log scheduled tasks
        logger.info(f"📋 Scheduled {len(self.scheduled_tasks)} tasks:")
        for task in self.scheduled_tasks.values():
            status = "✅ Enabled" if task.enabled else "❌ Disabled"
            logger.info(f"   {task.name}: {task.schedule_expression} - {status}")

        # Main scheduler loop
        while self.is_running:
            try:
                await self._check_and_run_due_tasks()
                await asyncio.sleep(60)  # Check every minute

            except KeyboardInterrupt:
                logger.info("⏹️ Scheduler shutdown requested")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)

        await self.stop_scheduler()

    async def stop_scheduler(self):
        """Stop the ETL scheduler"""
        logger.info("⏹️ Stopping AHAII ETL Scheduler...")

        self.is_running = False

        # Cancel all running tasks
        for task_id, task in self.running_tasks.items():
            logger.info(f"🛑 Cancelling running task: {task_id}")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        self.running_tasks.clear()
        logger.info("✅ ETL Scheduler stopped")

    async def _check_and_run_due_tasks(self):
        """Check for due tasks and execute them"""
        now = datetime.now()

        for task_id, task in self.scheduled_tasks.items():
            # Skip if disabled or already running
            if not task.enabled or task_id in self.running_tasks:
                continue

            # Check if task is due
            if task.next_run and now >= task.next_run:
                logger.info(f"⏰ Running due task: {task.name}")

                # Start the task
                async_task = asyncio.create_task(self._execute_task(task))
                self.running_tasks[task_id] = async_task

                # Update task metadata
                task.last_run = now
                task.next_run = self._calculate_next_run(
                    task.schedule_type, task.schedule_expression
                )
                task.run_count += 1
                task.updated_at = now

                logger.info(f"📅 Next run for {task.name}: {task.next_run}")

    async def _execute_task(self, task: ScheduledTask):
        """Execute a scheduled task with timeout and error handling"""
        task_start = datetime.now()

        try:
            logger.info(f"▶️ Starting task: {task.name}")

            # Execute with timeout
            result = await asyncio.wait_for(
                task.pipeline_function(), timeout=task.timeout_minutes * 60
            )

            duration = datetime.now() - task_start
            logger.info(
                f"✅ Task completed: {task.name} ({duration.total_seconds():.1f}s)"
            )

            # Send success notification if configured
            if task.notify_on_success:
                await self._send_notification(task, "success", result)

            # Reset failure count on success
            task.failure_count = 0

        except asyncio.TimeoutError:
            duration = datetime.now() - task_start
            error_msg = f"Task timed out after {task.timeout_minutes} minutes"
            logger.error(f"⏰ {error_msg}: {task.name}")

            task.failure_count += 1
            await self._handle_task_failure(task, error_msg)

        except Exception as e:
            duration = datetime.now() - task_start
            error_msg = f"Task failed with error: {str(e)}"
            logger.error(f"❌ {error_msg}: {task.name}")

            task.failure_count += 1
            await self._handle_task_failure(task, error_msg)

        finally:
            # Remove from running tasks
            if task.task_id in self.running_tasks:
                del self.running_tasks[task.task_id]

    async def _handle_task_failure(self, task: ScheduledTask, error_msg: str):
        """Handle task failure with retries and notifications"""

        # Send failure notification
        if task.notify_on_failure:
            await self._send_notification(
                task,
                "failure",
                {"error": error_msg, "failure_count": task.failure_count},
            )

        # Disable task if max failures reached
        if task.failure_count >= task.max_failures:
            task.enabled = False
            logger.error(f"🚨 Task disabled due to repeated failures: {task.name}")

            # Send critical failure notification
            await self._send_notification(
                task,
                "critical_failure",
                {
                    "error": error_msg,
                    "failure_count": task.failure_count,
                    "max_failures": task.max_failures,
                },
            )
        else:
            # Schedule retry
            retry_time = datetime.now() + timedelta(minutes=task.retry_delay_minutes)
            task.next_run = retry_time
            logger.info(f"⏳ Retry scheduled for {task.name} at {retry_time}")

    async def _send_notification(self, task: ScheduledTask, status: str, data: Any):
        """Send task notification (placeholder for email/Slack integration)"""
        try:
            notification_data = {
                "timestamp": datetime.now().isoformat(),
                "task_name": task.name,
                "task_id": task.task_id,
                "status": status,
                "data": data,
                "run_count": task.run_count,
                "failure_count": task.failure_count,
            }

            logger.info(f"📧 Notification ({status}): {task.name}")
            # TODO: Implement actual email/Slack notification
            # For now, just log the notification
            logger.info(f"   Recipients: {task.notification_emails}")
            logger.info(
                f"   Data: {json.dumps(notification_data, indent=2, default=str)}"
            )

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

    def _validate_schedule_expression(
        self, schedule_type: ScheduleType, expression: str
    ) -> bool:
        """Validate schedule expression format"""
        try:
            if schedule_type == ScheduleType.INTERVAL:
                # Validate interval format (e.g., "6h", "30m", "1d")
                import re

                pattern = r"^(\d+)([hdm])$"  # hours, days, minutes
                return bool(re.match(pattern, expression))

            elif schedule_type == ScheduleType.CRON:
                # Validate cron expression (basic validation)
                parts = expression.split()
                return len(parts) == 5  # minute hour day month weekday

            elif schedule_type == ScheduleType.ONE_TIME:
                # Validate datetime format
                datetime.fromisoformat(expression)
                return True

            return False

        except Exception:
            return False

    def _calculate_next_run(
        self, schedule_type: ScheduleType, expression: str
    ) -> datetime:
        """Calculate next run time based on schedule"""
        now = datetime.now()

        try:
            if schedule_type == ScheduleType.INTERVAL:
                # Parse interval (e.g., "6h", "30m", "1d")
                import re

                match = re.match(r"^(\d+)([hdm])$", expression)
                if match:
                    value, unit = int(match.group(1)), match.group(2)
                    if unit == "h":
                        return now + timedelta(hours=value)
                    elif unit == "d":
                        return now + timedelta(days=value)
                    elif unit == "m":
                        return now + timedelta(minutes=value)

            elif schedule_type == ScheduleType.CRON:
                # Basic cron parsing (would need proper cron library for production)
                # For now, use simple patterns
                if expression == "0 2 * * *":  # Daily at 2 AM
                    next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)
                    if next_run <= now:
                        next_run += timedelta(days=1)
                    return next_run

                elif expression == "0 6,18 * * *":  # 6 AM and 6 PM
                    next_6am = now.replace(hour=6, minute=0, second=0, microsecond=0)
                    next_6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)

                    if now < next_6am:
                        return next_6am
                    elif now < next_6pm:
                        return next_6pm
                    else:
                        return next_6am + timedelta(days=1)

                elif expression == "0 1 * * 0":  # Sunday at 1 AM
                    next_run = now.replace(hour=1, minute=0, second=0, microsecond=0)
                    days_until_sunday = (6 - now.weekday()) % 7
                    if days_until_sunday == 0 and next_run <= now:
                        days_until_sunday = 7
                    return next_run + timedelta(days=days_until_sunday)

            elif schedule_type == ScheduleType.ONE_TIME:
                return datetime.fromisoformat(expression)

        except Exception as e:
            logger.error(f"Failed to calculate next run time: {e}")

        # Default fallback
        return now + timedelta(hours=1)

    # Pipeline execution methods
    async def _run_news_monitoring(self):
        """Execute news monitoring pipeline"""
        return await self.orchestrator.run_news_monitoring_pipeline()

    async def _run_academic_processing(self):
        """Execute academic processing pipeline"""
        return await self.orchestrator.run_academic_processing_pipeline()

    async def _run_scoring(self):
        """Execute scoring pipeline"""
        return await self.orchestrator.run_scoring_pipeline()

    async def _run_data_quality_check(self):
        """Execute data quality check"""
        return await self.quality_manager.run_comprehensive_quality_check()

    async def _run_full_pipeline(self):
        """Execute complete ETL pipeline"""
        return await self.orchestrator.run_full_pipeline()

    # Status and monitoring methods
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status and statistics"""
        uptime = (
            datetime.now() - self.startup_time if self.startup_time else timedelta(0)
        )

        return {
            "is_running": self.is_running,
            "uptime_seconds": uptime.total_seconds(),
            "startup_time": (
                self.startup_time.isoformat() if self.startup_time else None
            ),
            "total_tasks": len(self.scheduled_tasks),
            "enabled_tasks": sum(
                1 for task in self.scheduled_tasks.values() if task.enabled
            ),
            "running_tasks": len(self.running_tasks),
            "task_summary": [
                {
                    "task_id": task.task_id,
                    "name": task.name,
                    "enabled": task.enabled,
                    "schedule": task.schedule_expression,
                    "last_run": task.last_run.isoformat() if task.last_run else None,
                    "next_run": task.next_run.isoformat() if task.next_run else None,
                    "run_count": task.run_count,
                    "failure_count": task.failure_count,
                    "is_running": task.task_id in self.running_tasks,
                }
                for task in self.scheduled_tasks.values()
            ],
        }

    async def run_task_now(self, task_id: str) -> bool:
        """Run a specific task immediately"""
        if task_id not in self.scheduled_tasks:
            logger.error(f"Task not found: {task_id}")
            return False

        if task_id in self.running_tasks:
            logger.error(f"Task already running: {task_id}")
            return False

        task = self.scheduled_tasks[task_id]
        logger.info(f"🚀 Running task on demand: {task.name}")

        # Start the task
        async_task = asyncio.create_task(self._execute_task(task))
        self.running_tasks[task_id] = async_task

        return True


async def start_etl_scheduler():
    """Main entry point to start the ETL scheduler"""
    scheduler = AHAIIETLScheduler()

    try:
        await scheduler.start_scheduler()
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted by user")
    finally:
        await scheduler.stop_scheduler()


if __name__ == "__main__":
    # Start the ETL scheduler
    asyncio.run(start_etl_scheduler())
