import type { EventFilters } from '../api/client';

interface Props {
  filters: EventFilters;
  setFilters: (next: EventFilters) => void;
  useMyLocation: () => void;
}

export function Filters({ filters, setFilters, useMyLocation }: Props) {
  return (
    <section className="filters">
      <input
        type="date"
        value={filters.from || ''}
        onChange={(e) => setFilters({ ...filters, from: e.target.value })}
      />
      <select
        value={filters.type || ''}
        onChange={(e) => setFilters({ ...filters, type: e.target.value || undefined })}
      >
        <option value="">Todos los tipos</option>
        <option value="trail">Trail</option>
        <option value="road">Road</option>
        <option value="running">Running</option>
      </select>
      <input
        type="number"
        placeholder="Distancia mínima"
        value={filters.distanceMin ?? ''}
        onChange={(e) =>
          setFilters({ ...filters, distanceMin: e.target.value ? Number(e.target.value) : undefined })
        }
      />
      <input
        type="number"
        placeholder="Distancia máxima"
        value={filters.distanceMax ?? ''}
        onChange={(e) =>
          setFilters({ ...filters, distanceMax: e.target.value ? Number(e.target.value) : undefined })
        }
      />
      <input
        type="number"
        placeholder="Radio km"
        value={filters.radius ?? ''}
        onChange={(e) => setFilters({ ...filters, radius: e.target.value ? Number(e.target.value) : undefined })}
      />
      <button onClick={useMyLocation}>Usar mi ubicación</button>
    </section>
  );
}
