import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment'; // adjust path if needed

@Injectable({
  providedIn: 'root',
})
export class SharedService {
  private apiUrl = `${environment.apiUrl}/employee/`;

  constructor(private http: HttpClient) {}

  getAllEmployees(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

}
