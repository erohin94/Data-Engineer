При удалении папки, выскакивает предупреждение

![image](https://github.com/user-attachments/assets/c70fe0c5-804a-4c13-ae99-6a66be140117)

В результате чего удалить не возможно. Поэтому удаляем програмно

Определяем путь к папке

```
import os
os.getcwd()
```

И удаляем
```
import shutil
shutil.rmtree('путь к папке')
```
