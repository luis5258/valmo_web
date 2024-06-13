from django.shortcuts import redirect,render
from django.contrib import messages
from django.db.models import Sum
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from Aplicacion.views import agregarDatosTecnicos
from Aplicacion.views import servicioActivo, grupo_user
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Q
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< GUARDAR FORMULARIO PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# -------------------------------------------------ENTRADA MATERIAS PRIMAS-------------------------------------------------
def guardarEntradaMateriaPrima(request):
    clave = request.POST['clave']
    proveedor_v = request.POST['proveedor']
    almacen_v = request.POST['almacen']
    presentacion_v = request.POST['presentacion']
    materiaPrima_v = request.POST['materiaPrima']
    cantidad_v = request.POST['cantidad']
    referencia_v = request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    clave_int = int(clave)
    formatoClave = 'EMP-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Entrada Materias Primas'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    if referencia_v == '':
        referencia_v = 0

    chofer_v = request.POST['chofer']      
    tblEntradaMP.objects.create(
    IDFolio = formatoClave, IDProveedor_id = proveedor_v, IDAlmacen_id = almacen_v, IDMateriaPrima_id = materiaPrima_v,
    IDPresentacion_id = presentacion_v, cantidad = cantidad_v, referencia = referencia_v,
    fecha = fecha_v, notas = notas_v)
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, 'La Entrada de Materias Primas se ha registrado exitosamente')

    if chofer_v != '':
        operador_V= request.POST['operador']    
        camion_V= request.POST['camion']    
        placas_V= request.POST['placas']    
        costo_V= request.POST['costo']    
        flete_V= request.POST['flete']    
        maniobra_V= request.POST['maniobra']  
        if costo_V == '':
            costo_V = 0.0
        if flete_V == '':
            flete_V = 0.0
        if maniobra_V == '':
            maniobra_V = 0.0
        tblOtrosDatosMovMP.objects.create(
            IDMovMP = formatoClave, IDOperador_id = operador_V, Costo = costo_V, Flete = flete_V,
            Maniobra = maniobra_V, Camion = camion_V, Chofer = chofer_v, Placas = placas_V
        )
        messages.success(request, f'Se ha añadido el operador "{chofer_v}" correctamente')
    else:
        operador_V= request.POST['operador'] 
        tblOtrosDatosMovMP.objects.create(
            IDMovMP = formatoClave, IDOperador_id = operador_V, Costo = 0, Flete = 0,
            Maniobra = 0, Camion = "", Chofer = "", Placas = ""
        )
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Ent-Materia-Prima')
        elif 'agregar' in request.POST:
            return redirect('F-Ent-Materia-Prima')
    else:
        return redirect('T-Ent-Materia-Prima')

def guardarSalidasMateriaPrima(request):
    clave = request.POST['clave']
    cliente_v = request.POST['cliente']
    # almacen_v = request.POST['almacen']
    presentacion_v = request.POST['presentacion']
    materiaPrima_v = request.POST['materiaPrima']
    cantidad_v = request.POST['cantidad']
    referencia_v = request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    if referencia_v == '':
        referencia_v = 0

    clave_int = int(clave)
    formatoClave = 'SMP-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Salidas Materias Primas'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    chofer_v = request.POST['chofer']      
    if chofer_v != '':
        operador_V= request.POST['operador']    
        camion_V= request.POST['camion']    
        placas_V= request.POST['placas']    
        tblOtrosDatosSalXBas.objects.create(
            IDSalida = formatoClave, IDOperador_id = operador_V, Camion = camion_V, 
            Chofer = chofer_v, Placas = placas_V
        )
        messages.success(request, f'Se ha añadido el operador "{chofer_v}" correctamente')
    else:
        operador_V= request.POST['operador'] 
        tblOtrosDatosSalXBas.objects.create(
            IDSalida = formatoClave, IDOperador_id = operador_V, Camion = "", Chofer = "", Placas = ""
        )

    tblSalidaMP.objects.create(
    IDFolio = formatoClave, IDCliente_id = cliente_v, IDAlmacen_id = 3, 
    IDMateriaPrima_id = materiaPrima_v, IDPresentacion_id = presentacion_v, cantidad = cantidad_v, 
    referencia = referencia_v, fecha = fecha_v, notas = notas_v)

    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, 'La Salida de Materias Primas se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Sal-Materia-Prima')
        elif 'agregar' in request.POST:
            return redirect('F-Sal-Materia-Prima')
    else:
        return redirect('T-Sal-Materia-Prima')

def guardarEntradaBasculas(request):
    clave_v = request.POST['clave']
    proveedor_v = request.POST['proveedor']
    almacen_v = request.POST['almacen']
    presentacion_v = request.POST['presentacion']
    productos_v = request.POST['productos']
    cantidad_v = request.POST['cantidad']
    referencia_v= request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    clave_int = int(clave_v)
    formatoClave = 'EP-{:06d}'.format(clave_int)

    if referencia_v == '':
        referencia_v = 0
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Entrada Productos'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave_v

    tblEntradaProductos.objects.create(
        IDFolio=formatoClave, IDProveedor_id=proveedor_v, IDAlmacen_id=almacen_v, IDProductos_id=productos_v,
        IDPresentacion_id=presentacion_v, cantidad=cantidad_v, referencia=referencia_v,fecha = fecha_v,
        notas=notas_v
    )
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    chofer_v = request.POST['chofer']    
    if chofer_v != '':
        operador_V= request.POST['operador']    
        camion_V= request.POST['camion']    
        placas_V= request.POST['placas']    
        costo_V= request.POST['costo']    
        flete_V= request.POST['flete']    
        maniobra_V= request.POST['maniobra']  
        if costo_V == '':
            costo_V = 0.0
        if flete_V == '':
            flete_V = 0.0
        if maniobra_V == '':
            maniobra_V = 0.0
        tblOtrosDatosMovMP.objects.create(
            IDMovMP = formatoClave, IDOperador_id = operador_V, Costo = costo_V, Flete = flete_V,
            Maniobra = maniobra_V, Camion = camion_V, Chofer = chofer_v, Placas = placas_V
        )
        messages.success(request, f'Se ha añadido el operador "{chofer_v}" correctamente')
    else:
        operador_V= request.POST['operador'] 
        tblOtrosDatosMovMP.objects.create(
            IDMovMP = formatoClave, IDOperador_id = operador_V, Costo = 0, Flete = 0,
            Maniobra = 0, Camion = "", Chofer = "", Placas = ""
        )
    messages.success(request, 'La Entrada de productos se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Ent-Productos')
        elif 'agregar' in request.POST:
            return redirect('F-Ent-Productos')
    else:
        return redirect('T-Ent-Productos')
    
def guardarSalidaBasculas(request):
    clave_v = request.POST['clave']
    cliente_v = request.POST['cliente']
    almacen_v = 3
    presentacion_v = request.POST['presentacion']
    productos_v = request.POST['productos']
    cantidad_v = request.POST['cantidad']
    referencia_v= request.POST['referencia']
    fecha_v = request.POST['fecha']
    notas_v = request.POST['notas']

    clave_int = int(clave_v)
    formatoClave = 'SP-{:06d}'.format(clave_int)

    if referencia_v == '':
        referencia_v = 0
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Salidas Productos'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave_v

    tblSalidaProductos.objects.create(
        IDFolio=formatoClave, IDCliente_id=cliente_v, IDAlmacen_id=almacen_v, IDProductos_id=productos_v,
        IDPresentacion_id=presentacion_v, cantidad=cantidad_v, referencia=referencia_v,fecha = fecha_v,
        notas=notas_v
    )
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    chofer_v = request.POST['chofer']    
    if chofer_v != '':
        operador_V= request.POST['operador']    
        camion_V= request.POST['camion']    
        placas_V= request.POST['placas']    
        
        tblOtrosDatosSalXBas.objects.create(
            IDSalida = formatoClave, IDOperador_id = operador_V, Camion = camion_V, 
            Chofer = chofer_v, Placas = placas_V
        )
        messages.success(request, f'Se ha añadido el operador "{chofer_v}" correctamente')
        
    else:
        operador_V= request.POST['operador'] 
        tblOtrosDatosSalXBas.objects.create(
            IDSalida = formatoClave, IDOperador_id = operador_V, Camion = "", Chofer = "", Placas = ""
        )
    salidaMP(request, productos_v, cantidad_v, cliente_v, almacen_v, presentacion_v, fecha_v, notas_v, formatoClave, referencia_v)        
    messages.success(request, 'La Salida de productos se ha registrado exitosamente')

    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Sal-Productos')
        elif 'agregar' in request.POST:
            return redirect('F-Sal-Productos')
    else:
        return redirect('T-Sal-Productos')

def salidaMP(request, productos_v, cantidad_v, cliente_v, almacen_v, presentacion_v, fecha_v, notas_v, formatoClave, referencia_v):
    Recetas = tblProductosMateriaPrima.objects.filter(IDProductos_id = productos_v).values('ID', 'Folio',
    'IDMateriaPrima_id__Descripcion', 'Merma', 'Porcentaje', 'IDMateriaPrima_id')
    ultimo_id = tblSalidaMP.objects.order_by('-ID').first()       
    if ultimo_id:
        ultimo_folio = ultimo_id.ID
    else:
        ultimo_folio = 0
    for receta in Recetas:
        ultimo_folio += 1
        formatoClaves = 'B-{:06d}'.format(ultimo_folio)
        cantidad = float(cantidad_v)    
        # Imprime los valores de cada campo
        proporcion  = cantidad * (receta['Porcentaje'] / 100) * ((receta['Merma'] / 100) + 1)
        materia_prima = receta['IDMateriaPrima_id']
        Referencia = receta['Folio']
        TEContenedorProductos = tblContenedoresProductos.objects.get(ID=almacen_v)
        Almacen = TEContenedorProductos.IDCliente.ID
        tblSalidaMP.objects.create( IDFolio = formatoClaves, IDCliente_id = cliente_v, IDAlmacen_id = 3, 
        IDMateriaPrima_id = materia_prima, IDPresentacion_id = presentacion_v, cantidad = proporcion, 
        referencia = 1, fecha = fecha_v, notas = notas_v)

def salidaMPServidos(request):
    # Filtrar los objetos que deseas
    servidos = tblServido.objects.filter(IDEstatus_id=10)

    if servidos.exists():
        # Anotar la suma de CantidadServida agrupada por IDProducto_id
        servidos_agrupados = servidos.values('IDCliente_id','IDProducto_id').annotate(total_servido=Sum('CantidadServida'))
        ultimo_id = tblSalidaMP.objects.order_by('-ID').first()
        if ultimo_id:
            ultimo_folio = ultimo_id.ID
        else:
            ultimo_folio = 0
        # Ahora tienes un queryset con la suma de CantidadServida agrupada por IDProducto_id
        for item in servidos_agrupados:
            
            productos_v = item['IDProducto_id']
            cantidad_v = item['total_servido']
            cliente_v = item['IDCliente_id']
            print(cliente_v, productos_v)
            if cliente_v == 3:
                almacen_v = 4
            elif cliente_v == 4:
                almacen_v = 5
            else:
                almacen_v = 3

            presentacion_v = 3
            fecha_v = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    
            Recetas = tblProductosMateriaPrima.objects.filter(IDProductos_id = productos_v).values('ID', 'Folio',
            'IDMateriaPrima_id__Descripcion', 'Merma', 'Porcentaje', 'IDMateriaPrima_id')
            for receta in Recetas:
                ultimo_folio += 1
                formatoClave = 'S-{:06d}'.format(ultimo_folio)
                cantidad = float(cantidad_v)    
                # Imprime los valores de cada campo
                proporcion  = cantidad * (receta['Porcentaje'] / 100) * ((receta['Merma'] / 100) + 1)
                materia_prima = receta['IDMateriaPrima_id']
                Referencia = receta['Folio']

                tblSalidaMP.objects.create( IDFolio = formatoClave, IDCliente_id = cliente_v, IDAlmacen_id = almacen_v, 
                IDMateriaPrima_id = materia_prima, IDPresentacion_id = presentacion_v, cantidad = proporcion, 
                referencia = 1, fecha = fecha_v)
        servidos = tblServido.objects.filter(IDEstatus_id=10).update(IDEstatus_id = 11)
    return redirect('T-Corrales-Servidos')

# -------------------------------------------------MOVIMIENTOS DE ANIMALES-------------------------------------------------
def guardarMovimientos(request):
    clave = request.POST['clave']
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)
    folio_Existe = tblMovimientoAnimales.objects.filter(Folio=formatoClave).exists()
    ServiciosWeb = servicioActivo()
    
    AgMovimientos = tblMovimientoAnimales.objects.get(ID=clave)
    Cliente = AgMovimientos.IDCliente.ID
    Corral = AgMovimientos.IDCorral.ID
    Movimiento = AgMovimientos.IDMovimiento.ID
    FiltradoCliente = tblClientes.objects.get(ID=Cliente)
    FiltradoCorral = tblCorrales.objects.get(ID=Corral)
    FiltradoMovimiento = tblTipoMov.objects.get(ID=Movimiento)
    FTipoAnimal = tblAnimalesTipo.objects.all()
    Detalle = tblDetalleMovAnimales.objects.filter(IDFolio=formatoClave).values('IDFolio', 'IDAnimales_id__Descripcion', 'Cantidad')
    animal = request.POST['animal']
    cantidad = request.POST['cantidad']

    ultimo_id = tblDetalleMovAnimales.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Cantidad Movimientos Animales'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = ultimo_folio
    
    tblDetalleMovAnimales.objects.create(
        IDFolio = formatoClave, IDAnimales_id = animal, Cantidad = cantidad
    )
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, f'Se ha agregado exitosamente el registro de {cantidad} animal(es)')
    
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-MovAnimales')
        elif 'agregar' in request.POST:
            return render(request, "Procesos/MovimientosAnimales/agregar.html", {'formatoClave':formatoClave, 'ServiciosWeb': ServiciosWeb, 
            'Detalle':Detalle,'AgMovimientos': AgMovimientos, 'FiltradoCliente':FiltradoCliente, 
            'FiltradoCorral':FiltradoCorral, 'FiltradoMovimiento':FiltradoMovimiento, 'FTipoAnimal':FTipoAnimal })
    else:
        return redirect('T-MovAnimales')


def guardarMovimientoAniamles(request):
    clave = request.POST['clave']
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)
    folio_Existe = tblMovimientoAnimales.objects.filter(Folio=formatoClave).exists()

    cliente = request.POST['cliente']
    corral = request.POST['corral']
    movimiento = request.POST['movimiento']
    peso = request.POST['peso']
    guia = request.POST['guia']
    partida = request.POST['partida']
    fecha = request.POST['fecha']
    notas = request.POST['notas']

    animal = request.POST['animal']
    cantidad = request.POST['cantidad']

    if guia == '':
        guia = 0
    if partida == '':
        partida = 0
        
    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Movimientos Animales'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    FTipoAnimal = tblAnimalesTipo.objects.all()
    Agrego_aniamles = { 'clave':clave, 'cliente':cliente, 'corral':corral, 'movimiento':movimiento,
        'peso':peso, 'guia':guia, 'partida':partida, 'fecha':fecha, 'notas':notas }
    ServiciosWeb = servicioActivo()
    
    if request.method == 'POST':
        if 'salir' in request.POST:
            tblMovimientoAnimales.objects.create(
                Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id = corral, IDMovimiento_id = movimiento,  
                Fecha = fecha, Peso = peso, NoPartida = partida, No_Guia = guia, Notas = notas
            )
            if cantidad != '':
                tblDetalleMovAnimales.objects.create(
                    IDFolio = formatoClave, IDAnimales_id = animal, Cantidad = cantidad
                )
            agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
            messages.success(request, f'El movimiento de animales  ha sido registrado exitosamente')
            return redirect('T-MovAnimales')
        
        elif 'agregar' in request.POST:
            tblMovimientoAnimales.objects.create(
                Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id = corral, IDMovimiento_id = movimiento,  
                Fecha = fecha, Peso = peso, NoPartida = partida, No_Guia = guia, Notas = notas
            )
            if cantidad != '0' or cantidad != 0 or cantidad != '':
                tblDetalleMovAnimales.objects.create(
                    IDFolio = formatoClave, IDAnimales_id = animal, Cantidad = cantidad
                )
            agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
            messages.success(request, f'El movimiento de animales  ha sido registrado exitosamente')
            return redirect('F-MovAnimales')
        
        elif 'guardarAnimal' in request.POST:
            folio_Existe = tblMovimientoAnimales.objects.filter(Folio=formatoClave).exists()
            Detalle = tblDetalleMovAnimales.objects.filter(IDFolio=formatoClave).values('IDFolio', 'IDAnimales_id__Descripcion', 'Cantidad')
            FiltradoCliente= tblClientes.objects.get(ID=cliente)
            FiltradoCorral= tblCorrales.objects.get(ID=corral)
            FiltradoMovimiento = tblTipoMov.objects.get(ID=movimiento)
            if folio_Existe:
                tblDetalleMovAnimales.objects.create(
                    IDFolio = formatoClave, IDAnimales_id = animal, Cantidad = cantidad
                )
                messages.success(request, f'El animal se guardo el animal correctamente')
            else:
                tblMovimientoAnimales.objects.create(
                    Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id = corral, IDMovimiento_id = movimiento,  
                    Fecha = fecha, Peso = peso, NoPartida = partida, No_Guia = guia, Notas = notas
                )
                tblDetalleMovAnimales.objects.create(
                    IDFolio = formatoClave, IDAnimales_id = animal, Cantidad = cantidad
                )
                agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
                messages.success(request, f'El movimiento se ha registrado exitosamente')
            return render(request, "Procesos/MovimientosAnimales/form.html", {'formatoClave':formatoClave,'Agrego_aniamles':Agrego_aniamles, 
                    'Detalle':Detalle,'ultimo_folio': clave, 'folio_Existe':folio_Existe, 'FTipoAnimal':FTipoAnimal, 'ServiciosWeb': ServiciosWeb, 
                    'FiltradoCliente':FiltradoCliente,'FiltradoCorral':FiltradoCorral,'FiltradoMovimiento':FiltradoMovimiento })
    else:
        return redirect('T-MovAnimales')

# -------------------------------------------------DETALLES DE ANIMALES-------------------------------------------------
# ESTA FUNCION NO ESTA LISTA
def guardarDetallesAniamles(request):
    clave = request.POST['clave']
    cliente = request.POST['cliente']
    corral = request.POST['corral']
    movimiento = request.POST['movimiento']
    animal = request.POST['animal']
    cantidad = request.POST['cantidad']
    peso = request.POST['peso']
    guia = request.POST['guia']
    partida = request.POST['partida']
    fecha = request.POST['fecha']
    notas = request.POST['notas']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)
    IDFila_v = clave

    tblMovimientoAnimales.objects.create(
        Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id = corral, IDAnimal_id = animal,
        IDMovimiento_id = movimiento,  Fecha = fecha, Cantidad = cantidad, Peso = peso,
        NoPartida = partida, No_Guia = guia, Notas = notas
    )
    
    messages.success(request, 'El Movimiento de animales se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-MovAnimales')
        elif 'agregar' in request.POST:
            return redirect('F-MovAnimales')
    else:
        return redirect('T-MovAnimales')

def guardarSolicitudServido(request):
    clave = request.POST['folio']
    cliente = request.POST['cliente']
    corral = request.POST['corral']
    producto = request.POST['producto']
    estatus = request.POST['estatus']
    prioridad = request.POST['prioridad']
    cantidadSol = request.POST['cantidadSol']
    cantidadSer = request.POST['cantidadSer']
    fechaSol = request.POST['fechaSol']
    fechaSer = request.POST['fechaSer']
    
    peticion = request.POST['peticion']

    
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Servidos Manuales'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    tblServido.objects.create(Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id =corral, IDProducto_id = producto, 
    IDEstatus_id = estatus, CantidadSolicitada = cantidadSol, CantidadServida =cantidadSer, 
    Prioridad =prioridad, Fecha = fechaSol, FechaServida = fechaSer) 
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, 'El Servido Manual se ha registrado exitosamente')
    if request.method == 'POST':
        if peticion == '1' or peticion == 1:
            if 'salir' in request.POST:
                return redirect('T-Solicitud-Servidos')
            elif 'agregar' in request.POST:
                ultimo_contacto = tblServido.objects.order_by('-ID').first()
                if ultimo_contacto:
                    ultimo_folio = ultimo_contacto.ID + 1
                else:
                    ultimo_folio = 1
                cantidadSol = request.POST['cantidadSol']
                SelectProducto = tblProductos.objects.get(ID = producto)
                SelectCorral = tblCorrales.objects.get(ID = corral)
                SelectCliente = tblClientes.objects.get(ID = cliente)
                FClientes = tblClientes.objects.exclude(ID = 1).all().order_by('Nombre')
                FECorrales = tblCorrales.objects.exclude(Q(IDCliente= 1) | (Q(ID =1))).order_by('Descripcion')
                FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
                FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
                FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
                print(cantidadSol)

                return render(request, 'Procesos/Solicitud Servido/form.html',{'FClientes':FClientes,
                'ultimo_folio': ultimo_folio, 'SelectCliente':SelectCliente, 'SelectCorral':SelectCorral, 'SelectProducto':SelectProducto,                                                                         
                'cantidadSol':cantidadSol, 'FECorrales':FECorrales, 'FEProductos':FEProductos, 'FEstatus':FEstatus, 'FechaDeHoy':FechaDeHoy})
        elif peticion == '2' or peticion == 2:
            email = request.POST['email']            
            request.session['email'] = email
            return redirect('FP-Cliente')
    else:
        return redirect('T-Solicitud-Servidos')
    
# -------------------------------------------------SERVIDOS MANUALES-------------------------------------------------
def guardarServidosManuales(request):
    clave = request.POST['folio']
    cliente = request.POST['cliente']
    corral = request.POST['corral']
    producto = request.POST['producto']
    estatus = request.POST['estatus']
    prioridad = request.POST['prioridad']
    cantidadSol = request.POST['cantidadSol']
    cantidadSer = request.POST['cantidadSer']
    fechaSol = request.POST['fechaSol']
    fechaSer = request.POST['fechaSer']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Servidos Manuales'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    tblServido.objects.create(Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id =corral, IDProducto_id = producto, 
    IDEstatus_id = estatus, CantidadSolicitada = cantidadSol, CantidadServida =cantidadSer, 
    Prioridad =prioridad, Fecha = fechaSol, FechaServida = fechaSer
    ) 
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, 'El Servido Manual se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Servidos')
        elif 'agregar' in request.POST:
            return redirect('F-Servidos')
    else:
        return redirect('T-Servidos')

# -------------------------------------------------INVENTARIOS MATERIA PRIMAS-------------------------------------------------
def guardarInventarioMateriaPrima(request):
    clave = request.POST['clave']
    almacen = request.POST['almacen']
    materia = request.POST['materia']
    fecha = request.POST['fecha']
    cantidad = request.POST['cantidad']
    notas = request.POST['notas']
 
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Inventario Materia Prima'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    tblInventarioInicialesMP.objects.create(
        Folio = formatoClave, IDContenedor_id  = almacen, IDMateriaPrima_id= materia, 
        Cantidad  = cantidad, Fecha = fecha, Notas = notas
    ) 
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, 'El Inventario Materia Prima se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-InventarioMP')
        elif 'agregar' in request.POST:
            return redirect('F-InventarioMP')
    else:
        return redirect('T-InventarioMP')

def guardarInventarioProductos(request):
    clave = request.POST['clave']
    almacen = request.POST['almacen']
    producto = request.POST['producto']
    fecha = request.POST['fecha']
    cantidad = request.POST['cantidad']
    notas = request.POST['notas']
  
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Inventario Productos'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    tblInventarioInicialesProductos.objects.create(
        Folio = formatoClave, IDContenedor_id = almacen, IDProducto_id = producto, 
        Cantidad  = cantidad, Fecha = fecha, Notas = notas
    ) 
    agregarDatosTecnicos(request, Tecnico_v, NombreTabla_v, IDFilaTabla_v, AreaRegistro_v, IDFila_v)
    messages.success(request, 'El Inventario de productos se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-InventarioProductos')
        elif 'agregar' in request.POST:
            return redirect('F-InventarioProductos')
    else:
        return redirect('T-InventarioProductos')