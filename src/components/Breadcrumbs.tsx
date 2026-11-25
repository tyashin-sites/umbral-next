import Link from 'next/link';

export function Breadcrumbs({ items }: { items: { name: string; href?: string }[] }) {
  return (
    <nav aria-label="Breadcrumb" className="text-[0.72rem] uppercase tracking-[0.2em] text-muted">
      <ol className="flex flex-wrap items-center gap-3">
        <li><Link href="/" className="link-line">Umbral</Link></li>
        {items.map((c) => (
          <li key={c.name} className="flex items-center gap-3">
            <span aria-hidden="true" className="h-px w-4 bg-current opacity-50" />
            {c.href ? <Link href={c.href} className="link-line">{c.name}</Link> : <span aria-current="page" className="text-foreground">{c.name}</span>}
          </li>
        ))}
      </ol>
    </nav>
  );
}
