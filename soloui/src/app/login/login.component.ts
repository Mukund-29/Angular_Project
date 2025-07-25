import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

@Component({
  standalone: true,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports: [CommonModule, FormsModule],
})
export class LoginComponent {
  ntid = '';
  password = '';
  error = '';

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  login(): void {
    const payload = { NTID: this.ntid, password: this.password };

    this.http.post<any>(`${environment.apiUrl}/token/`, payload).subscribe({
      next: (res) => {
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem('access_token', res.access);
          localStorage.setItem('refresh_token', res.refresh);

          if (res.user) {
            localStorage.setItem('user', JSON.stringify(res.user));
          }
        }
        this.error = '';
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.error = err.status === 401 ? 'Invalid NTID or Password' : 'Server error. Try again later.';
      },
    });
  }

  isLoggedIn(): boolean {
    return isPlatformBrowser(this.platformId) && !!localStorage.getItem('access_token');
  }
}
