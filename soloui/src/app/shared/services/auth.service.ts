import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  login(ntid: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/token/`, { NTID: ntid, password });
  }

  logout(refresh: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/logout/`, { refresh });
  }
}
