'use client';
import { useState } from 'react';
import { submitLead } from '@/lib/leads';
import { SYSTEMS } from '@/data/collection';

type Status = 'idle' | 'sending' | 'sent' | 'error';

export function QuoteForm({ system, kind = 'quote' }: { system?: string; kind?: 'quote' | 'architect' }) {
  const [status, setStatus] = useState<Status>('idle');
  const [error, setError] = useState('');
  const current = SYSTEMS.find((s) => s.slug === system);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const get = (k: string) => String(fd.get(k) ?? '').trim();
    if (get('website')) return; // honeypot
    setStatus('sending');
    setError('');
    const sys = SYSTEMS.find((s) => s.slug === get('system'));
    try {
      await submitLead({
        name: get('name'),
        email: get('email'),
        phone: get('phone') || undefined,
        subject: kind === 'architect' ? `Architect request — ${sys?.name ?? 'general'}` : `Quotation — ${sys?.name ?? 'general enquiry'}`,
        message: get('message') || '(no message)',
        source: kind === 'architect' ? 'umbral-architects' : 'umbral-quotation',
        customFields: {
          role: get('role'),
          system: sys?.name ?? '',
          width_mm: get('width'),
          height_mm: get('height'),
          finish: get('finish'),
          project_location: get('location'),
        },
      });
      setStatus('sent');
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'We could not send that.');
    }
  }

  if (status === 'sent') {
    return (
      <div className="border-t border-border pt-10" role="status">
        <p className="t-h2">Thank you.</p>
        <p className="t-body mt-4">We read every enquiry ourselves. Expect a considered reply, with questions about the opening, within two working days.</p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-8 md:grid-cols-2" noValidate={false}>
      <div className="field"><label htmlFor="q-name">Name</label><input id="q-name" name="name" required autoComplete="name" /></div>
      <div className="field"><label htmlFor="q-email">Email</label><input id="q-email" name="email" type="email" required autoComplete="email" /></div>
      <div className="field">
        <label htmlFor="q-role">You are</label>
        <select id="q-role" name="role" defaultValue={kind === 'architect' ? 'Architect' : 'Homeowner'}>
          <option>Homeowner</option><option>Architect</option><option>Builder</option><option>Interior designer</option><option>Dealer</option>
        </select>
      </div>
      <div className="field"><label htmlFor="q-phone">Phone (optional)</label><input id="q-phone" name="phone" type="tel" autoComplete="tel" /></div>
      <div className="field">
        <label htmlFor="q-system">System</label>
        <select id="q-system" name="system" defaultValue={current?.slug ?? ''}>
          <option value="">Not sure yet</option>
          {SYSTEMS.map((s) => (<option key={s.slug} value={s.slug}>{s.name}</option>))}
        </select>
      </div>
      <div className="field"><label htmlFor="q-location">Project location</label><input id="q-location" name="location" placeholder="City, country" /></div>
      <div className="field"><label htmlFor="q-width">Opening width (mm)</label><input id="q-width" name="width" inputMode="numeric" pattern="[0-9]*" /></div>
      <div className="field"><label htmlFor="q-height">Opening height (mm)</label><input id="q-height" name="height" inputMode="numeric" pattern="[0-9]*" /></div>
      {current?.finishes?.length ? (
        <div className="field md:col-span-2">
          <label htmlFor="q-finish">Finish</label>
          <select id="q-finish" name="finish" defaultValue={current.finishes[0]}>
            {current.finishes.map((f) => (<option key={f}>{f}</option>))}
          </select>
        </div>
      ) : <input type="hidden" name="finish" value="" />}
      <div className="field md:col-span-2"><label htmlFor="q-message">{kind === 'architect' ? 'What do you need — sections, BIM, specification text?' : 'Tell us about the opening'}</label><textarea id="q-message" name="message" /></div>
      <input type="text" name="website" tabIndex={-1} autoComplete="off" aria-hidden="true" className="hidden" />
      <div className="flex flex-wrap items-center gap-6 md:col-span-2">
        <button type="submit" className="btn btn-primary" disabled={status === 'sending'}>
          {status === 'sending' ? 'Sending' : kind === 'architect' ? 'Request documents' : 'Request a quotation'} <span className="arrow" aria-hidden="true" />
        </button>
        <p className="text-[0.8rem] text-muted">We use your details only to answer this enquiry. <a href="/privacy" className="link-line">Privacy</a></p>
        {status === 'error' ? <p role="alert" className="w-full text-[0.9rem] text-[#8a3b2a]">{error}</p> : null}
      </div>
    </form>
  );
}
