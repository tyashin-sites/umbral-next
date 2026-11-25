'use client';
import { useEffect } from 'react';
import { usePathname } from 'next/navigation';

/**
 * One IntersectionObserver for every `.reveal` on the page. Content is visible
 * without JS: the hidden state only exists under html.js, set here.
 */
export function RevealObserver() {
  const pathname = usePathname();
  useEffect(() => {
    // Anything already on screen stays put (no hide-then-show flash); only
    // what is still below the fold waits to settle in.
    const vh = window.innerHeight;
    document.querySelectorAll<HTMLElement>('.reveal:not(.is-in)').forEach((e) => {
      if (e.getBoundingClientRect().top < vh * 0.92) e.classList.add('is-in');
    });
    document.documentElement.classList.add('js');
    const els = Array.from(document.querySelectorAll<HTMLElement>('.reveal:not(.is-in)'));
    if (!('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -12% 0px' });
    els.forEach((e) => io.observe(e));
    return () => io.disconnect();
  }, [pathname]);
  return null;
}
