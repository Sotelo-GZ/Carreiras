import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import type { EventItem } from '../types/event';
import 'leaflet/dist/leaflet.css';

interface Props {
  events: EventItem[];
}

const GALICIA_CENTER: [number, number] = [42.8, -8.3];

export function EventsMap({ events }: Props) {
  return (
    <MapContainer center={GALICIA_CENTER} zoom={8} scrollWheelZoom className="map">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {events.map((event) => (
        <Marker key={event.id} position={[event.latitude, event.longitude]}>
          <Popup>
            <strong>{event.name}</strong>
            <br />
            {new Date(event.date).toLocaleDateString()} · {event.distance_km} km
            <br />
            {event.type}
            <br />
            <a href={event.source_url} target="_blank" rel="noreferrer">
              Ver carrera
            </a>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
