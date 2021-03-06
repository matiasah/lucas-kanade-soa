import { Component, ViewChild } from '@angular/core';
import { HttpClient, HttpRequest, HttpResponse } from '@angular/common/http';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  private host = 'http://localhost:5000/';

  // Video que se va a subir para analizar
  public video: any;

  // Video de la respuesta (conjunto de imágenes con el resultado)
  public videoResponse: any;  

  // Ruta de descarga del vide procesado
  public downloadPath: string;

  // Indicar que se encuentra enviando el video
  public enviando = false;

  // Formulario
  @ViewChild('form', { static: true })
  public form: NgForm;

  public constructor(
    private http: HttpClient
  ) {

  }

  public onSubmit() {
    // Indicar que se encuentra enviando
    this.enviando = true;
    // Formulario para enviar el video
    const formData = new FormData();

    // Insertar el video en el formulario
    formData.append('video', this.video);

    // Construir el request para enviar
    const req = new HttpRequest('POST', this.host + 'lucas-kanade', formData, { responseType: 'json' });

    // Enviar la peticion post al servicio de lucas kanade
    this.http.request<any>(req).subscribe(
      Response => {
        // Convertir el Response HttpEvent a un objeto any
        this.videoResponse = Response as any;

        // Extraer el cuerpo de la respuesta
        this.videoResponse = this.videoResponse.body;

        if (this.videoResponse) {
          // Indicar que ya se recivió la respuesta
          this.enviando = false;

          // Ruta de descarga del video
          this.downloadPath = this.host + "video-output/" + this.video.name;

        }
      },
      Error => {
        this.enviando = false;
        console.log(Error);
      }
    );
  }

  public handleFileInput(files: FileList) {
    this.video = files.item(0);
    this.videoResponse = undefined;
  }

  public extractBase64(imagen: any) {
    imagen.imagen = imagen.imagen.substring(2, imagen.imagen.length - 1);
    return 'data:image/png;base64,' + imagen.imagen;
  }
}

