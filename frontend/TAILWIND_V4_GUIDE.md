# AHAII TailwindCSS v4 Implementation Guide

## Overview
This guide explains how to use the comprehensive TailwindCSS v4 theme system implemented for the African Health AI Infrastructure Index (AHAII) project. The system includes a step gradient background, domain-specific colors for the four pillars, KPI indicators, chart colors, and consistent animation strategies.

## Key Features

### 1. **Step Gradient Background System**
The main background uses a beautiful step gradient from dark to light (top to bottom):
- `bg-section-1`: Darkest (#0f172a)
- `bg-section-2`: Medium-dark (#1e293b) 
- `bg-section-3`: Medium-light (#334155)
- `bg-section-4`: Lightest (#475569)

### 2. **Four Pillar Domain Colors**
Each assessment domain has its own color scheme:
- **Physical Infrastructure**: Emerald Green (`--color-physical`)
- **Human Capital**: Sky Blue (`--color-human-capital`)
- **Legal & Regulatory**: Purple (`--color-regulatory`)
- **Economic Potential**: Orange (`--color-economic`)

### 3. **KPI Traffic Light System**
Performance indicators use a traffic light color system:
- `kpi-excellent`: Green (#22c55e)
- `kpi-good`: Lime (#84cc16)
- `kpi-fair`: Yellow (#eab308)
- `kpi-warning`: Orange (#f97316)
- `kpi-poor`: Red (#ef4444)
- `kpi-critical`: Dark Red (#dc2626)

### 4. **Chart & Visualization Colors**
Complementary colors for data visualization:
- `chart-1` through `chart-8`: Distinct colors for graphs and charts

### 5. **Adaptive Text System**
Text colors automatically adapt to different background sections:
- `text-paragraph-section-1`: Light text for dark backgrounds
- `text-paragraph-section-2`: Medium-light text
- `text-paragraph-section-3`: Medium text
- `text-paragraph-section-4`: Darker text for lighter backgrounds

## Usage Examples

### Basic Layout Structure
```tsx
<div className="min-h-screen bg-section-1">
  {/* Hero section with darkest background */}
  <section className="section bg-section-1">
    <div className="container">
      <h1 className="text-foreground">Hero Title</h1>
      <p className="text-paragraph-section-1">Hero description</p>
    </div>
  </section>

  {/* Content section with medium background */}
  <section className="section bg-section-2">
    <div className="container">
      <h2 className="text-foreground">Section Title</h2>
      <p className="text-paragraph-section-2">Section content</p>
    </div>
  </section>
</div>
```

### Domain-Specific Styling
```tsx
{/* Physical Infrastructure Card */}
<div className="card domain-physical">
  <div className="domain-icon">
    <ServerIcon className="w-6 h-6" />
  </div>
  <h3>Physical Infrastructure</h3>
  <div className="domain-badge">30% weight</div>
</div>

{/* Human Capital Card */}
<div className="card domain-human-capital">
  <div className="domain-icon">
    <UsersIcon className="w-6 h-6" />
  </div>
  <h3>Human Capital</h3>
  <div className="domain-badge">30% weight</div>
</div>
```

### KPI Indicators
```tsx
{/* KPI Badges */}
<div className="kpi-badge kpi-badge-excellent">Excellent</div>
<div className="kpi-badge kpi-badge-good">Good</div>
<div className="kpi-badge kpi-badge-fair">Fair</div>
<div className="kpi-badge kpi-badge-poor">Poor</div>

{/* KPI Text Colors */}
<span className="kpi-excellent">95% Score</span>
<span className="kpi-warning">60% Score</span>
<span className="kpi-critical">25% Score</span>
```

### Cards with Hover Effects
```tsx
<div className="card card-hover">
  <div className="card-header">
    <h3 className="card-title">Card Title</h3>
    <p className="card-description">Card description</p>
  </div>
  <div className="card-content">
    Card content goes here
  </div>
</div>
```

### Gradient Text
```tsx
<h1 className="text-gradient gradient-primary">
  Gradient Text
</h1>
<h2 className="text-gradient gradient-human-capital">
  Human Capital Focus
</h2>
```

### Data Visualization Components
```tsx
<div className="chart-container">
  <div className="data-card">
    <div className="data-card-title">Readiness Score</div>
    <div className="data-card-value">78</div>
    <div className="data-card-trend data-card-trend-up">
      ↗ +5.2%
    </div>
  </div>
</div>
```

## Animation System

### Built-in CSS Animations
Use these classes for smooth animations:
```tsx
{/* Fade effects */}
<div className="animate-fade-in">Content fades in</div>
<div className="animate-slide-up">Content slides up</div>
<div className="animate-slide-down">Content slides down</div>
<div className="animate-slide-left">Content slides from left</div>
<div className="animate-slide-right">Content slides from right</div>
<div className="animate-scale-up">Content scales up</div>

{/* With delays and custom durations */}
<div className="animate-fade-in animate-delay-200 animate-duration-500">
  Delayed fade in
</div>
```

### Framer Motion Integration
```tsx
import { motion } from 'framer-motion';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

<motion.div
  initial="initial"
  whileInView="animate"
  viewport={{ once: true }}
  variants={staggerContainer}
>
  <motion.h2 variants={fadeInUp}>Title</motion.h2>
  <motion.p variants={fadeInUp}>Description</motion.p>
</motion.div>
```

## Button System
```tsx
{/* Primary buttons */}
<button className="btn btn-primary">Primary Action</button>
<button className="btn btn-secondary">Secondary Action</button>
<button className="btn btn-outline">Outline Button</button>
<button className="btn btn-ghost">Ghost Button</button>

{/* Domain-specific buttons */}
<button className="btn btn-domain domain-physical">
  Physical Infrastructure Action
</button>
```

## Layout Utilities
```tsx
{/* Container and section spacing */}
<div className="container"> {/* Max-width container with padding */}
  <section className="section"> {/* Responsive padding */}
    Content here
  </section>
</div>

{/* Flexbox utilities */}
<div className="flex-center">Centered content</div>
<div className="flex-between">Space between content</div>
<div className="flex-center-y">Vertically centered</div>

{/* Responsive visibility */}
<div className="only-mobile">Mobile only</div>
<div className="only-tablet">Tablet only</div>
<div className="only-desktop">Desktop only</div>
```

## Icon Integration
Your custom SVG icons are located in `/images/svg-icons/` and organized by:
- `country-icons/`: African country icons
- `other-icons/`: General purpose icons (medical, technical, etc.)

```tsx
<img 
  src="/images/svg-icons/other-icons/server-icon-light.svg"
  alt="Physical Infrastructure"
  className="w-6 h-6"
/>
```

## Accessibility Features
```tsx
{/* Screen reader only content */}
<span className="sr-only">Screen reader description</span>

{/* Focus-only visible content */}
<div className="focus-only">Only visible when focused</div>

{/* High contrast focus styles */}
<button className="focus-visible">Accessible button</button>
```

## Color Customization
All colors are defined as CSS custom properties and can be accessed directly:
```css
/* Use in custom components */
.custom-component {
  background-color: var(--color-physical);
  border-color: var(--color-physical-400);
  color: var(--color-physical-700);
}
```

## Performance Considerations
1. **Dynamic imports**: Use for heavy components
2. **Animation delays**: Stagger animations to avoid overwhelming users
3. **Viewport-based animations**: Use `whileInView` for scroll-triggered animations
4. **CSS custom properties**: Enable dynamic theming and consistent colors

## Migration from v3
If you have existing TailwindCSS v3 code:
1. Replace `bg-gradient-to-b from-slate-900 to-slate-700` with `bg-section-1`
2. Replace custom color classes with domain-specific ones
3. Use the new animation utilities instead of custom CSS
4. Leverage the card system instead of custom card styles

This system provides a cohesive, professional appearance that reinforces the AHAII brand while maintaining excellent accessibility and performance.
