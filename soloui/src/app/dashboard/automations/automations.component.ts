import { Component, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-automations',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './automations.component.html',
  styleUrls: ['./automations.component.css'],
})
export class AutomationsComponent {
  @ViewChild('carousel', { static: false }) carousel!: ElementRef;
  searchTerm: string = '';

  constructor(private router: Router) {}

  items = [
    {
      title: 'Bill Estimate Comparison',
      description: 'The Bill Estimate Comparison automation extracts and compares text from two PDFs — the estimated bill and the actual bill — to highlight any discrepancies. It uses a backend service that parses both documents, aligns line items, and flags differences in amounts, quantities, or descriptions. This reduces manual effort by 100% and improves accuracy by 99%, enabling teams, management, and clients to quickly validate billing data.',
      route: 'bill-estimate-compare'
    },
    {
      title: 'Automation 2',
      description: 'Details about Automation 2',
      route: '',
    },
    {
      title: 'Automation 3',
      description: 'Details about Automation 3',
      route: '',
    },
        {
      title: 'Automation 4',
      description: 'Details about Automation 2',
      route: '',
    },
    {
      title: 'Automation 5',
      description: 'Details about Automation 3',
      route: '',
    },
    {
      title: 'Automation 6',
      description: 'Details about Automation 2',
      route: '',
    },
    {
      title: 'Automation 7',
      description: 'Details about Automation 3',
      route: '',
    },
      {
      title: 'Automation 8',
      description: 'Details about Automation 2',
      route: '',
    },
    {
      title: 'Automation 9',
      description: 'Details about Automation 3',
      route: '',
    },
    // other items...
  ];

  filteredItems() {
    return this.items.filter(item =>
      item.title.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  scrollLeft() {
    this.carousel.nativeElement.scrollBy({ left: -300, behavior: 'smooth' });
  }

  scrollRight() {
    this.carousel.nativeElement.scrollBy({ left: 300, behavior: 'smooth' });
  }

  // ✅ Correct route relative to /dashboard/automations
  navigateTo(route: string): void {
    if (route) {
      this.router.navigate(['dashboard', 'automations', route]);
    }
  }
}
