import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { SharedService } from '../shared/services/shared.service';

@Component({
  selector: 'app-employee',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './employee.component.html',
  styleUrls: ['./employee.component.css'],
})
export class EmployeeComponent implements OnInit {
  employeeList: any[] = [];
  ntid: string = '';
  firstName: string = '';
  email: string = '';
  unitName: string = '';

  constructor(
    private sharedService: SharedService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

ngOnInit(): void {
  this.sharedService.getAllEmployees().subscribe((data) => {
    this.employeeList = data;
  });

  if (isPlatformBrowser(this.platformId)) {
    const userRaw = localStorage.getItem('user');
    console.log('🟢 Raw user from localStorage:', userRaw); // Log raw value

    try {
      if (userRaw) {
        const user = JSON.parse(userRaw);
        console.log('🟢 Parsed user:', user); // ✅ Log parsed user
        this.ntid = user.NTID || '';
        this.firstName = user.First_Name || '';
        this.email = user.Email_Id || '';
        this.unitName = user.Unit_Name || '';
      } else {
        console.warn('⚠️ user key is not present in localStorage');
      }
    } catch (e) {
      console.error('❌ Error parsing user:', e);
    }
  }
}


  isLoggedIn(): boolean {
    return isPlatformBrowser(this.platformId) && !!localStorage.getItem('access_token');
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      console.clear();
    }
    this.router.navigate(['/']);
  }
}
