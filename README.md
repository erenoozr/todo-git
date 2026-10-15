# todo-git

Koddaki `TODO`, `FIXME`, `HACK`, `XXX` ve `shortcut:` notlarını tarar, tek sayfalık bir HTML rapor üretir.
Rapor açık ve koyu temaya uyar, etiket başına özet gösterir.

## Kullanım

Python 3.8+ yeterli, ek paket gerekmez.

```
python todo_git.py C:\Dev\projem
python todo_git.py C:\Dev\projem -o rapor.html
```

Varsayılan çıktı, çalıştırdığın klasördeki `todo-rapor.html` dosyasıdır.

## Neyi yakalar?

- Büyük harfle ve tam kelime olarak yazılmış `TODO`, `FIXME`, `HACK`, `XXX`. `todos` ya da `XXXL` gibi kelimeler eşleşmez.
- Küçük harfle `shortcut:` biçimindeki notlar.

## Neyi atlar?

- `.git`, `node_modules`, `venv`, `.venv`, `dist`, `build`, `__pycache__` klasörleri. Bu klasörlerin içine hiç girilmez.
- 1 MB'tan büyük dosyalar ve ikili dosyalar.
- Raporun kendisi, taranan klasörün içine yazılsa bile.

UTF-8 olmayan metin dosyaları da taranır; bozuk karakterler `?` olarak görünür.

## Sınırlar

Satır bazlı regex ile arar ve satırın yorum olup olmadığına bakmaz. Örneğin bir string içindeki `TODO` da yakalanır.

## Geliştirme

```
pip install pytest
python -m pytest tests
```

Lisans: MIT
