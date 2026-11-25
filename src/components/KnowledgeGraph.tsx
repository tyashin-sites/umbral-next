import { buildGraph } from '@/lib/knowledge-graph';

export function KnowledgeGraph(props: Parameters<typeof buildGraph>[0]) {
  const json = JSON.stringify(buildGraph(props)).replace(/</g, '\\u003c').replace(/>/g, '\\u003e');
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: json }} />;
}
