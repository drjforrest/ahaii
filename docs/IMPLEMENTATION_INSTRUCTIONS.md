# AHAII Landing Page Implementation Instructions

## Overview
Replace the current `/frontend/src/app/page.tsx` with a compelling narrative-driven homepage that demonstrates the academic foundation and health-specific focus of AHAII.

## Key Requirements

### 1. Dependencies
Ensure these are installed in the frontend:
```bash
npm install framer-motion
```

### 2. Component Structure
The page consists of 6 main sections:
1. **Hero Section** (bg-section-1): Problem statement with statistics
2. **Problem Amplification** (bg-section-2): AI gap widening 
3. **Academic Foundation** (bg-section-3): Building on existing scholarship
4. **Solution Introduction** (bg-section-4): Four domains framework
5. **Four Pillars Showcase** (bg-section-2): Interactive domain exploration
6. **Call to Action** (bg-section-1): "If we don't measure, we guess"

### 3. Animation Strategy
- Use Framer Motion for scroll-triggered animations
- Implement `whileInView` with `viewport={{ once: true }}`
- Stagger children animations for visual appeal
- Add hover states for interactive elements

### 4. Icon Integration
All icons should use the established light variants from `/images/svg-icons/other-icons/`:
- Use semantic icon choices that reinforce content
- Maintain consistent sizing (16px, 20px, 24px, 32px, 48px)
- Leverage dark/light variants appropriately for background sections

### 5. Typography & Styling
- Use established Tailwind v4 gradient text classes: `text-gradient gradient-primary`, `gradient-physical`, etc.
- Follow section background progression: `bg-section-1` → `bg-section-2` → `bg-section-3` → `bg-section-4`
- Use adaptive text colors: `text-paragraph-section-1` through `text-paragraph-section-4`
- Implement domain-specific styling: `domain-physical`, `domain-human-capital`, etc.

### 6. Interactive Elements
- Four pillars should have hover states revealing additional information
- Use `useState` to track active pillar
- Implement smooth transitions for pillar details
- Add click functionality for navigation to other pages

### 7. Responsive Design
- Mobile-first approach with progressive enhancement
- Grid layouts should collapse appropriately on smaller screens
- Ensure touch-friendly interactions
- Optimize for African connectivity patterns

## Critical Implementation Notes

### Academic Credibility
The "Academic Foundation" section is crucial—it establishes that AHAII builds on proven methodology from IMF, Oxford Insights, and UNESCO, but adapts it specifically for health infrastructure needs.

### Narrative Flow
The page tells a story:
1. **Problem**: Africa's health burden vs. limited AI benefit
2. **Context**: General AI readiness frameworks exist but miss health specifics
3. **Solution**: AHAII's four-domain approach fills this gap
4. **Impact**: Evidence-based measurement enables strategic deployment
5. **Urgency**: Without measurement, we guess—and guessing costs lives

### Performance Considerations
- Optimize images for various connection speeds
- Use lazy loading for non-critical images
- Implement smooth scroll behavior
- Add loading states for interactive elements

## File Locations
- Main component: `/frontend/src/app/page.tsx`
- Icons: `/frontend/src/public/images/svg-icons/other-icons/`
- Styles: Already configured in `/frontend/src/app/globals.css`

## Testing Checklist
- [ ] All animations work smoothly
- [ ] Icons load correctly and match design intent
- [ ] Responsive design works across devices
- [ ] Hover states provide clear feedback
- [ ] Navigation links function properly
- [ ] Performance is acceptable on slower connections
- [ ] Color contrast meets accessibility standards

## Next Steps After Implementation
1. Test across different devices and browsers
2. Verify accessibility compliance
3. Optimize performance metrics
4. Connect navigation to other pages (About, Methods, Dashboard)
5. Add analytics tracking for user engagement

The goal is a professional, academically credible homepage that clearly communicates AHAII's value while maintaining the sophisticated design system you've established.
