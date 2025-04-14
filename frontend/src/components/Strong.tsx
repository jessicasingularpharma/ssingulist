import React, { ReactNode } from 'react';

export const Strong = ({ children }: { children: ReactNode }) => (
  <strong className="font-semibold text-gray-900">{children}</strong>
);
