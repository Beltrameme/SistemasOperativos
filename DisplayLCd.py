import requests, json, serial, time

ser = serial.Serial( #configuraciones para leer el puerto serie de la rasp
    port='COM4',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_TWO,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("conectado al puerto: " + ser.portstr)

api_key = "2222cb3869cd1a47a0d25817ea7dc627"

ciudad = input("Ingresa el nombre de tu ciudad : ")

coordenadas = "http://api.openweathermap.org/geo/1.0/direct?q=" + ciudad + "&limit=5&appid=" + api_key

coordResponse = requests.get(coordenadas)

if coordResponse.status_code == 200:
  v = coordResponse.content.decode('utf-8')
  m = json.loads(v)
  print("encontramos mas de una ciudad con ese nombre", ciudad, ":")
  for i, location in enumerate(m):
      print(f"{i + 1}. {location['name']}, {location['country']}")

  elegida = int(input("Ingresa el numero de tu ciudad deseada (o 0 para salir): "))

  if elegida > 0 and elegida <= len(m):
      latitud = m[elegida - 1]["lat"]
      longitud = m[elegida - 1]["lon"]

else:
    print("Error: No pudimos devolver las coordenadas, revisa tu API KEY o tu conexion a internet")

def pedido_info (lat,lon):
    temps = "https://api.openweathermap.org/data/2.5/weather?" + "lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + api_key
    tempResponse = requests.get(temps)

    x = tempResponse.json()

    if x["cod"] != "404":
        y = x["main"]
        temperatura = y["temp"]
        humedad = y["humidity"]
        z = x["weather"]
        clima = z[0]["description"]
        print(" Temperatura = " +
                        str(round(temperatura - 273.15,1)) +
            "\n humedad = " +
                        str(humedad) +
            "\n descripcion = " +
                        str(clima))
        return temperatura, humedad, clima
    else:
        print(" City Not Found ")

while True:
    datos = pedido_info(latitud, longitud)
    base = ciudad + "/" + "temp: " + str(round(datos[0] - 273.15, 1)) + " C"
    expandido = "hum: " + str(datos[1]) + "%" + "/" + datos[2]
    ser.write(bytes(base, 'utf-8'))
    time.sleep(5)
    ser.write(bytes(expandido, 'utf-8'))
    time.sleep(5)

