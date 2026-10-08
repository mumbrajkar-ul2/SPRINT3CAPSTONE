export class ApiService {
  baseUrl = '/api';
  getRecord(id: string) { return fetch(`${this.baseUrl}/records/${id}`); }
  summarize(id: string) { return fetch(`${this.baseUrl}/ai/summarize/${id}`, { method: 'POST' }); }
}
