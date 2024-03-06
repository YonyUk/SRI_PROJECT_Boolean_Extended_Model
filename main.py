from datetime import datetime
from models import ExtendedBooleanModel

def PrintResult(ranking):
    for document in ranking:
        print(f'\t\t\t\t{document[0]}')
        print(f'Ranking:\t\t\t\t\t {document[1]}')
        pass
    pass

print('Cargando base de datos')
t_init = datetime.now()
model = ExtendedBooleanModel(2)
t_end = datetime.now()
t = t_end - t_init
print(f'Cargada en {t}')
while True:
    try:
        result = model.Search(input('>>> '))
        PrintResult(result)
        pass
    except Exception:
        print('Hubo un error')
        pass
    pass