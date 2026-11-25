'use client';
import { useEffect } from 'react';

/** Toggles .is-scrolled on the header (class only — bar height is constant, CLS law). Also marks <html class="js"> for reveals. */
export function HeaderFX() {
  useEffect(() => {
    const header = document.querySelector('.site-header');
    const onScroll = () => header?.classList.toggle('is-scrolled', window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  return null;
}
