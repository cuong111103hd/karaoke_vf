import React from 'react';

interface StatusBadgeProps {
  status: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  let badgeClass = 'badge-pending';
  const label = status.toUpperCase();

  if (status === 'starting') {
    badgeClass = 'badge-starting';
  } else if (status === 'active' || status === 'processing') {
    badgeClass = 'badge-active animate-pulse';
  } else if (status === 'completed' || status === 'ready') {
    badgeClass = 'badge-completed';
  } else if (status === 'failed') {
    badgeClass = 'badge-failed';
  }

  return <span className={`status-badge ${badgeClass}`}>{label}</span>;
};
