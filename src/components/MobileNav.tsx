'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';

export function MobileNav({ items }: { items: readonly { label: string; href: string }[] }) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  useEffect(() => setOpen(false), [pathname]);
  useEffect(() => {
    document.documentElement.style.overflow = open ? 'hidden' : '';
    return () => { document.documentElement.style.overflow = ''; };
  }, [open]);
  return (
    <div className="md:hidden">
      <button type="button" aria-expanded={open} aria-controls="mobile-menu" onClick={() => setOpen((v) => !v)} className="relative z-[60] flex h-11 w-11 items-center justify-center" >
        <span className="sr-only">{open ? 'Close menu' : 'Open menu'}</span>
        <span aria-hidden="true" className="relative block h-3 w-7">
          <span className={`absolute left-0 right-0 top-0 h-px bg-current transition-transform duration-300 ${open ? 'translate-y-[6px] rotate-45' : ''}`} />
          <span className={`absolute left-0 right-0 bottom-0 h-px bg-current transition-transform duration-300 ${open ? '-translate-y-[5px] -rotate-45' : ''}`} />
        </span>
      </button>
      <div id="mobile-menu" hidden={!open} className="fixed inset-0 z-50 bg-cal">
        <nav className="wrap flex h-full flex-col justify-center gap-6" aria-label="Mobile">
          {items.map((i) => (
            <Link key={i.href} href={i.href} className="t-h1">{i.label}</Link>
          ))}
        </nav>
      </div>
    </div>
  );
}
