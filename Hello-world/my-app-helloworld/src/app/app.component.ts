import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Hello World';
  @ViewChild('bouncingContainer') bouncingContainer!: ElementRef;
  numImages = 20; // Ajusta la cantidad de imágenes en el mosaico
  imageSize = 50; // Debe coincidir con el width/height en CSS

  ngOnInit() {
    this.createBouncingImages();
    setInterval(() => {
      this.animateBouncingImages();
    }, 100); // Ajusta la velocidad de la animación (milisegundos)
  }

  createBouncingImages() {
    const container = this.bouncingContainer.nativeElement;
    const containerWidth = window.innerWidth;
    const containerHeight = window.innerHeight;

    for (let i = 0; i < this.numImages; i++) {
      const img = document.createElement('div');
      img.classList.add('bouncing-image');
      img.style.width = `${this.imageSize}px`;
      img.style.height = `${this.imageSize}px`;
      img.style.left = `${Math.random() * (containerWidth - this.imageSize)}px`;
      img.style.top = `${Math.random() * (containerHeight - this.imageSize)}px`;      
      img.dataset['vx'] = ((Math.random() - 0.5) * 2).toString(); // Velocidad inicial en X (-1 a 1)
      img.dataset['vy'] = ((Math.random() - 0.5) * 2).toString(); // Velocidad inicial en Y (-1 a 1)
      img.style.opacity = '1'; // Hacer visible la imagen
      container.appendChild(img);
    }
  }

  animateBouncingImages() {
    const container = this.bouncingContainer.nativeElement;
    const containerWidth = window.innerWidth;
    const containerHeight = window.innerHeight;
    const images = container.querySelectorAll('.bouncing-image');

    images.forEach((img: any) => {
      let x = parseFloat(img.style.left);
      let y = parseFloat(img.style.top);
      let vx = parseFloat(img.dataset['vx']);
      let vy = parseFloat(img.dataset['vy']);

      x += vx;
      y += vy;

      // Rebotar en los bordes
      if (x < 0 || x > containerWidth - this.imageSize) {
        vx *= -1;
      }
      if (y < 0 || y > containerHeight - this.imageSize) {
        vy *= -1;
      }
      img.style.left = `${x}px`;
      img.style.top = `${y}px`;
      img.dataset['vx'] = vx;
      img.dataset['vy'] = vy;
    });
  }  
}
