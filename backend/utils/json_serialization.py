"""
Comprehensive JSON Serialization Utility for AHAII Data Structures
Handles all pandas, numpy, and custom object serialization issues
"""

import json
import logging
from typing import Any, Dict, List, Union
from datetime import datetime, date
from decimal import Decimal
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class AHAIIJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that handles pandas and numpy objects
    """
    
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        elif pd.isna(obj):
            return None
        else:
            return super().default(obj)


def make_json_serializable(obj: Any) -> Any:
    """
    Convert any object to JSON-serializable format
    
    Handles:
    - Pandas DataFrames and Series
    - Numpy arrays and scalar types
    - Complex nested dictionaries with tuple keys
    - Custom objects with __dict__
    - Dataclasses
    - Datetime objects
    - Sets and other collections
    
    Args:
        obj: Object to make serializable
        
    Returns:
        JSON-serializable version of the object
    """
    
    # Handle None
    if obj is None:
        return None
    
    # Handle pandas NaN (only for scalar values)
    try:
        if pd.isna(obj):
            return None
    except (ValueError, TypeError):
        # pd.isna() fails on non-scalar values like DataFrames
        pass
    
    # Handle pandas DataFrames
    if isinstance(obj, pd.DataFrame):
        # Clean DataFrame before conversion
        df_clean = obj.copy()
        
        # Handle MultiIndex columns
        if isinstance(df_clean.columns, pd.MultiIndex):
            # Flatten MultiIndex columns
            df_clean.columns = ['_'.join(str(col).strip() for col in cols) 
                               for cols in df_clean.columns.values]
        
        # Handle MultiIndex in index
        if isinstance(df_clean.index, pd.MultiIndex):
            df_clean = df_clean.reset_index()
        
        # Convert any non-serializable columns
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].apply(
                    lambda x: make_json_serializable(x) if x is not None else None
                )
        
        return df_clean.to_dict('records')
    
    # Handle pandas Series
    elif isinstance(obj, pd.Series):
        # Handle MultiIndex Series
        if isinstance(obj.index, pd.MultiIndex):
            return {
                '_'.join(str(i) for i in key) if isinstance(key, tuple) else str(key): 
                make_json_serializable(val)
                for key, val in obj.items()
            }
        else:
            return {
                str(key): make_json_serializable(val)
                for key, val in obj.items()
            }
    
    # Handle pandas Index (including MultiIndex)
    elif isinstance(obj, pd.Index):
        return [make_json_serializable(item) for item in obj.tolist()]
    
    # Handle MultiIndex specifically
    elif isinstance(obj, pd.MultiIndex):
        return [list(make_json_serializable(item) for item in tup) for tup in obj.tolist()]
    
    # Handle numpy types
    elif isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
        # Handle NaN and infinity
        if np.isnan(obj) or np.isinf(obj):
            return None
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return [make_json_serializable(item) for item in obj.tolist()]
    
    # Handle Python built-in numeric types that might cause issues
    elif isinstance(obj, Decimal):
        return float(obj)
    
    # Handle datetime objects
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    
    # Handle tuples (convert to lists, handling nested complexity)
    elif isinstance(obj, tuple):
        return [make_json_serializable(item) for item in obj]
    
    # Handle sets (convert to lists)
    elif isinstance(obj, set):
        return [make_json_serializable(item) for item in sorted(list(obj))]
    
    # Handle dictionaries (including those with complex keys)
    elif isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            # Convert complex keys to strings
            if isinstance(k, tuple):
                key_str = '_'.join(str(item) for item in k)
            elif isinstance(k, (np.integer, np.floating, np.bool_)):
                key_str = str(k.item() if hasattr(k, 'item') else k)
            elif k is None:
                key_str = 'null'
            else:
                key_str = str(k)
            
            result[key_str] = make_json_serializable(v)
        return result
    
    # Handle lists
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    
    # Handle dataclasses
    elif hasattr(obj, '__dataclass_fields__'):
        return make_json_serializable(obj.__dict__)
    
    # Handle objects with __dict__ (custom objects)
    elif hasattr(obj, "__dict__"):
        return {k: make_json_serializable(v) for k, v in obj.__dict__.items()}
    
    # Handle Enums
    elif hasattr(obj, "value"):
        return make_json_serializable(obj.value)
    
    # Handle objects that have a to_dict method
    elif hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
        try:
            return make_json_serializable(obj.to_dict())
        except Exception as e:
            logger.warning(f"Failed to convert object to dict: {e}")
            return str(obj)
    
    # Handle objects that have an asdict method (like dataclasses)
    elif hasattr(obj, "__dict__") and hasattr(obj, "__annotations__"):
        try:
            from dataclasses import asdict
            return make_json_serializable(asdict(obj))
        except Exception:
            return make_json_serializable(obj.__dict__)
    
    # Test if already JSON serializable
    else:
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError, OverflowError) as e:
            logger.debug(f"Object not directly serializable: {type(obj)}, error: {e}")
            return str(obj)


def save_json(obj: Any, file_path: str, indent: int = 2) -> None:
    """
    Save object to JSON file with proper serialization
    
    Args:
        obj: Object to save
        file_path: Path to save the JSON file
        indent: JSON indentation level
    """
    try:
        serializable_obj = make_json_serializable(obj)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_obj, f, indent=indent, cls=AHAIIJSONEncoder, ensure_ascii=False)
        logger.info(f"Successfully saved JSON to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        raise


def load_json(file_path: str) -> Any:
    """
    Load JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded object
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {e}")
        raise


def test_serialization():
    """Test the serialization utility with various data types"""
    
    # Test data
    test_data = {
        'pandas_df': pd.DataFrame({
            'col1': [1, 2, np.nan, 4],
            'col2': ['a', 'b', 'c', 'd'],
            'col3': [1.1, 2.2, 3.3, np.inf]
        }),
        'pandas_series': pd.Series([1, 2, 3], index=['a', 'b', 'c']),
        'numpy_array': np.array([1, 2, 3]),
        'numpy_types': {
            'int64': np.int64(42),
            'float64': np.float64(3.14),
            'bool': np.bool_(True),
            'nan': np.nan,
            'inf': np.inf
        },
        'datetime': datetime.now(),
        'date': date.today(),
        'decimal': Decimal('123.45'),
        'tuple_key_dict': {
            ('a', 'b'): 'tuple_key_value',
            123: 'int_key_value'
        },
        'nested_complex': {
            'level1': {
                'level2': [
                    {'pandas_series': pd.Series([1, 2])},
                    np.array([4, 5, 6])
                ]
            }
        }
    }
    
    print("Testing JSON serialization...")
    
    try:
        serializable = make_json_serializable(test_data)
        json_str = json.dumps(serializable, indent=2)
        print("✅ Serialization successful!")
        print(f"JSON length: {len(json_str)} characters")
        
        # Test round-trip
        reloaded = json.loads(json_str)
        print("✅ Deserialization successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Serialization failed: {e}")
        return False


if __name__ == "__main__":
    test_serialization()
