/**
 * Paper Design System - Design Tokens
 * Centralized design token definitions for consistent styling
 */

export const colors = {
  // Primary palette
  primary: '#111111',
  secondary: '#8B5CF6',
  
  // Semantic colors
  success: '#16A34A',
  warning: '#D97706',
  danger: '#DC2626',
  
  // Surface and text
  surface: '#FFFFFF',
  text: '#111827',
  textLight: '#6B7280',
  textLighter: '#9CA3AF',
  
  // Borders and dividers
  border: '#E5E7EB',
  borderLight: '#F3F4F6',
  
  // Backgrounds
  background: '#FAFAFA',
} as const

export const typography = {
  fontFamily: {
    primary: '"Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    display: '"Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    mono: '"PT Mono", "SF Mono", Monaco, "Courier New", monospace',
  },
  scale: {
    xs: '14px',
    sm: '16px',
    md: '18px',
    lg: '24px',
    xl: '32px',
    xxl: '40px',
  },
  weights: {
    thin: 100,
    extralight: 200,
    light: 300,
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800,
    black: 900,
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '24px',
  xxl: '32px',
} as const

export const breakpoints = {
  mobile: '640px',
  tablet: '768px',
  desktop: '1024px',
  wide: '1280px',
} as const

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
} as const

export const radius = {
  sm: '2px',
  md: '4px',
  lg: '6px',
} as const
