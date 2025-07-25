import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { environment } from '@env/environment';

@Component({
  standalone: true,
  selector: 'app-bill-estimate-compare',
  templateUrl: './bill-estimate-compare.component.html',
  styleUrl: './bill-estimate-compare.component.css',
  imports: [CommonModule],
})
export class BillEstimateCompareComponent {
  file1: File | null = null;
  file2: File | null = null;
  lines1: string[] = [];
  lines2: string[] = [];
  uploadStatus = '';
  linePairs: [string, string][] = [];

  counts = {
    added: 0,
    removed: 0,
  };

  constructor(private http: HttpClient) {}

  onFileSelected(event: any, fileNumber: number) {
    const selectedFile = event.target.files[0];
    if (fileNumber === 1) this.file1 = selectedFile;
    else this.file2 = selectedFile;
  }

  uploadFiles() {
    if (!this.file1 || !this.file2) {
      this.uploadStatus = 'Please select both PDF files before uploading.';
      return;
    }

    const formData = new FormData();
    formData.append('file1', this.file1);
    formData.append('file2', this.file2);

    this.http.post<any>(`${environment.apiUrl}/upload-compare-pdfs/`, formData).subscribe({
      next: (response) => {
        this.uploadStatus = '✅ Files compared successfully!';
        this.lines1 = response.file1Lines;
        this.lines2 = response.file2Lines;
        this.linePairs = this.alignLines(this.lines1, this.lines2);
      },
      error: () => {
        this.uploadStatus = '❌ Failed to upload files.';
        this.lines1 = [];
        this.lines2 = [];
        this.linePairs = [];
      }
    });
  }

  alignLines(lines1: string[], lines2: string[]): [string, string][] {
    const pairs: [string, string][] = [];
    this.counts = { added: 0, removed: 0 };

    let i = 0;
    let j = 0;
    const maxLookahead = 3;

    while (i < lines1.length || j < lines2.length) {
      const line1 = lines1[i] || '';
      const line2 = lines2[j] || '';

      if (line1 === line2) {
        pairs.push([line1, line2]);
        i++;
        j++;
      } else {
        let foundMatch = false;

        // Look ahead for added lines
        for (let lookahead = 1; lookahead <= maxLookahead; lookahead++) {
          if (j + lookahead < lines2.length && lines1[i] === lines2[j + lookahead]) {
            for (let k = 0; k < lookahead; k++) {
              pairs.push(['', lines2[j]]);
              this.counts.added++; // green visual line
              j++;
            }
            foundMatch = true;
            break;
          }

          // Look ahead for removed lines
          if (i + lookahead < lines1.length && lines1[i + lookahead] === lines2[j]) {
            for (let k = 0; k < lookahead; k++) {
              pairs.push([lines1[i], '']);
              this.counts.removed++;
              i++;
            }
            foundMatch = true;
            break;
          }
        }

        if (!foundMatch) {
          pairs.push([line1, line2]);

          if (!line1 && line2) {
            this.counts.added++; // green visual line
          } else if (line1 && !line2) {
            this.counts.removed++;
          } else if (line1 !== line2) {
            this.counts.removed++;
          }

          i++;
          j++;
        }
      }
    }

    return pairs;
  }
}
