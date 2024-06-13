from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.templatetags.static import static
from datetime import datetime, timedelta, date
from Aplicacion.forms import *
from Aplicacion.models import *
from django.http import HttpResponse

def cargamento_tolva(request):
    
    fecha_actual = datetime.today()
    formatted_fecha_actual = fecha_actual.strftime("%Y-%m-%d %H-%M-%S")
    user = request.user
    logo_url = request.build_absolute_uri(static('assets/img/inicio/valmo.png'))
    
    tolva = request.POST.get('tolva', '')
    if tolva is not None and tolva != '':
        TTolva = tblTolva.objects.get(ID=tolva)
        producto = TTolva.IDProducto.ID
        FiltradoProducto= tblProductos.objects.get(ID=producto)
        unidad_id = FiltradoProducto.IDUnidadMedida.ID
        Filtradounidad= tblUnidades.objects.get(ID=unidad_id)
        TContenido = tblServido.objects.filter(IDEstatus_id = 8, IDTolva_id = tolva).order_by('ID').values('Folio',
        'IDCliente_id__Nombre', 'IDCorral_id__Descripcion','CantidadSolicitada', 'CantidadServida')
        print(TTolva.IDProducto.ID)
        
    # Render the HTML template with the data
    html_string = render_to_string('Descargas/PDF/index.html', {'logo_url': logo_url, 'Filtradounidad':Filtradounidad,
                                   'user': user,  'TContenido': TContenido, 'fecha_actual': fecha_actual, 'FiltradoProducto':FiltradoProducto})

    # Create a BytesIO buffer to receive the PDF
    pdf_buffer = BytesIO()

    # Generate the PDF using xhtml2pdf
    pisa.CreatePDF(html_string, dest=pdf_buffer)

    # Get the PDF content from the buffer
    pdf_file = pdf_buffer.getvalue()

    # Create an HTTP response with the attached PDF file
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Servidos {formatted_fecha_actual}.pdf"'
        # response['Content-Disposition'] = 'attachment; filename="Sálida-' + \
    #     Folio+" "+Nombre+'.pdf"'

    return response