import { PUBLIC_API_BASE } from '$env/static/public';

const API = PUBLIC_API_BASE || '';

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(API + path, init);
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) return res.json();
  // @ts-expect-error generic return for other types used in callers
  return res;
}

export type JobResp = { job_id: string };

export type Job = {
  job_id: string;
  status: string;
  upload_id?: string;
  processed_id?: string;
  latex_id?: string;
  pdf_id?: string;
};

export async function getJobs(): Promise<Job[]> {
  return await api<Job[]>('/api/jobs');
}

