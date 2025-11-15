# SVG Padding Remover / حذف‌کننده فضای خالی SVG

[English](#english) | [فارسی](#persian) | [📊 See Example](EXAMPLE.md)

---

## English

### Description

This script automatically removes extra padding from SVG files by calculating the actual bounding box of the content and adjusting the `viewBox` accordingly. It's perfect for cleaning up icon sets where icons have inconsistent padding.

### Features

- ✅ Automatically calculates the bounding box of SVG content
- ✅ Removes extra padding while preserving the artwork
- ✅ Supports batch processing of multiple SVG files
- ✅ Optional padding parameter to keep some space around content
- ✅ Preserves all SVG paths and transforms
- ✅ Makes SVG responsive by removing fixed width/height

### Installation

```bash
# Install required dependencies
pip install -r requirements.txt

# Or install manually
pip install svgpathtools
```

### Usage

#### Single File

```bash
# Basic usage - creates ic_activity_cropped.svg
python svg_crop.py ic_activity.svg

# Custom output name
python svg_crop.py ic_activity.svg output.svg

# With 10 units of padding
python svg_crop.py ic_activity.svg -p 10
```

#### Batch Processing

```bash
# Process all SVG files in current directory
python svg_crop.py --batch *.svg

# Process all SVGs from a folder to output folder
python svg_crop.py --batch icons/ output/

# Batch with padding
python svg_crop.py --batch icons/ output/ -p 5
```

### Example

**Before:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <path d="..."/>
</svg>
```

**After:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="53.33 -10.67 917.33 917.33">
  <path d="..."/>
</svg>
```

The script calculated that the actual content only needs a viewBox of `53.33 -10.67 917.33 917.33` instead of `0 0 1024 1024`, removing approximately 106 pixels of extra padding from the left, top, and right.

### Command Line Options

| Option | Description |
|--------|-------------|
| `input` | Input SVG file or pattern |
| `output` | Output SVG file or directory (optional) |
| `--batch`, `-b` | Process multiple files |
| `--padding`, `-p` | Padding to keep around content (default: 0) |

### How It Works

1. **Parse SVG**: Reads the SVG file and extracts all paths
2. **Calculate Bounding Box**: Uses svgpathtools to calculate the exact bounding box of all paths
3. **Adjust ViewBox**: Updates the viewBox to match the content bounds
4. **Save**: Writes the optimized SVG file

### Requirements

- Python 3.6+
- svgpathtools 1.6.0+
- numpy (installed automatically with svgpathtools)
- scipy (installed automatically with svgpathtools)

---

## Persian

<div dir="rtl">

### توضیحات

این اسکریپت به طور خودکار فضاهای خالی اضافی را از فایل‌های SVG حذف می‌کند. این کار با محاسبه Bounding Box واقعی محتوا و تنظیم `viewBox` انجام می‌شود. این ابزار برای تمیز کردن مجموعه آیکون‌هایی که فضای خالی ناهماهنگ دارند، عالی است.

### ویژگی‌ها

- ✅ محاسبه خودکار Bounding Box محتوای SVG
- ✅ حذف فضای خالی اضافی با حفظ طراحی اصلی
- ✅ پشتیبانی از پردازش دسته‌ای چندین فایل SVG
- ✅ پارامتر اختیاری برای نگه داشتن فضای خالی دلخواه
- ✅ حفظ تمام pathها و transformها
- ✅ ایجاد SVG واکنش‌گرا با حذف width/height ثابت

### نصب

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# یا نصب دستی
pip install svgpathtools
```

### نحوه استفاده

#### تک فایل

```bash
# استفاده ساده - فایل ic_activity_cropped.svg ایجاد می‌شود
python svg_crop.py ic_activity.svg

# با نام خروجی دلخواه
python svg_crop.py ic_activity.svg output.svg

# با 10 واحد فضای خالی
python svg_crop.py ic_activity.svg -p 10
```

#### پردازش دسته‌ای

```bash
# پردازش تمام فایل‌های SVG در پوشه فعلی
python svg_crop.py --batch *.svg

# پردازش تمام SVGها از یک پوشه به پوشه خروجی
python svg_crop.py --batch icons/ output/

# پردازش دسته‌ای با فضای خالی
python svg_crop.py --batch icons/ output/ -p 5
```

### مثال

**قبل:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <path d="..."/>
</svg>
```

**بعد:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="53.33 -10.67 917.33 917.33">
  <path d="..."/>
</svg>
```

اسکریپت محاسبه کرد که محتوای واقعی فقط به viewBox با مقدار `53.33 -10.67 917.33 917.33` نیاز دارد به جای `0 0 1024 1024`، که تقریباً 106 پیکسل فضای خالی اضافی از چپ، بالا و راست را حذف می‌کند.

### گزینه‌های خط فرمان

| گزینه | توضیحات |
|--------|---------|
| `input` | فایل یا الگوی ورودی SVG |
| `output` | فایل یا پوشه خروجی SVG (اختیاری) |
| `--batch`, `-b` | پردازش چند فایل |
| `--padding`, `-p` | فضای خالی برای نگه داشتن اطراف محتوا (پیش‌فرض: 0) |

### نحوه کار

1. **تجزیه SVG**: فایل SVG را می‌خواند و تمام pathها را استخراج می‌کند
2. **محاسبه Bounding Box**: از svgpathtools برای محاسبه دقیق bounding box استفاده می‌کند
3. **تنظیم ViewBox**: viewBox را به اندازه محتوا به‌روز می‌کند
4. **ذخیره**: فایل SVG بهینه‌شده را می‌نویسد

### نیازمندی‌ها

- Python 3.6 یا بالاتر
- svgpathtools 1.6.0 یا بالاتر
- numpy (به صورت خودکار با svgpathtools نصب می‌شود)
- scipy (به صورت خودکار با svgpathtools نصب می‌شود)

### نمونه‌های بیشتر

#### پردازش یک آیکون با حفظ 5 واحد فضای خالی
```bash
python svg_crop.py ic_activity.svg ic_activity_fixed.svg -p 5
```

#### پردازش کل پوشه آیکون‌ها
```bash
python svg_crop.py --batch ./icons/*.svg
```

#### پردازش و ذخیره در پوشه جدید
```bash
mkdir fixed_icons
python svg_crop.py --batch ./icons/ ./fixed_icons/
```

### نکات مهم

- ⚠️ همیشه قبل از پردازش دسته‌ای، یک نسخه پشتیبان از آیکون‌های خود تهیه کنید
- ℹ️ اگر SVG شما transformهای پیچیده دارد، ممکن است نیاز به بررسی دستی نتیجه باشد
- 💡 برای آیکون‌های UI معمولاً padding=0 بهترین گزینه است
- 🎨 برای لوگوها ممکن است padding کمی (مثلاً 5-10 واحد) بهتر باشد

### عیب‌یابی

**مشکل: فایل خروجی ایجاد نمی‌شود**
- بررسی کنید که svgpathtools نصب شده باشد: `pip list | grep svgpathtools`
- مطمئن شوید فایل ورودی یک SVG معتبر است

**مشکل: محتوای SVG بریده شده**
- از پارامتر padding استفاده کنید: `-p 10`
- بررسی کنید که transformهای SVG به درستی اعمال شده باشند

**مشکل: اسکریپت خیلی کند است**
- برای فایل‌های بزرگ، پردازش ممکن است کمی زمان ببرد
- می‌توانید فایل‌ها را به صورت موازی پردازش کنید

### مجوز

این اسکریپت آزاد و رایگان است و می‌توانید آن را برای هر منظوری استفاده کنید.

</div>

---

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

If you encounter any problems or have questions, please open an issue on the repository.
