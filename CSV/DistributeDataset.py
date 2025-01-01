import os
import shutil
import pandas as pd

def organize_pushup_images():
    """
    Organize push-up images into separate folders based on their classification
    from the _classes.csv file using absolute paths.
    """
    try:
        # Path absolut untuk direktori train dan file CSV
        train_dir = r"C:\Users\arsen\Protel\Dataset\pushup2\train"
        csv_file = os.path.join(train_dir, "_classes.csv")
        
        # Memastikan file dan direktori ada
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"File CSV tidak ditemukan di: {csv_file}")
        if not os.path.exists(train_dir):
            raise FileNotFoundError(f"Direktori train tidak ditemukan di: {train_dir}")
        
        # Membaca file CSV dan menampilkan informasi debug
        df = pd.read_csv(csv_file)
        print("\nInformasi CSV:")
        print("Nama kolom:", df.columns.tolist())
        print("\nContoh 5 baris pertama:")
        print(df.head())
        
        # Membuat folder untuk masing-masing kelas
        pushup_dir = os.path.join(train_dir, 'pushups')
        pushdown_dir = os.path.join(train_dir, 'pushdowns')
        
        # Membuat direktori jika belum ada
        os.makedirs(pushup_dir, exist_ok=True)
        os.makedirs(pushdown_dir, exist_ok=True)
        
        # Memproses setiap gambar
        successful_copies = 0
        failed_copies = 0
        
        for index, row in df.iterrows():
            filename = row['filename']
            # Menggunakan nama kolom yang benar dari CSV
            is_pushdown = row[df.columns[1]]  # Kolom kedua
            is_pushup = row[df.columns[2]]    # Kolom ketiga
            
            # Path sumber gambar
            src_path = os.path.join(train_dir, filename)
            
            try:
                # Memindahkan gambar ke folder yang sesuai
                if is_pushup == 1:
                    dst_path = os.path.join(pushup_dir, filename)
                    if os.path.exists(src_path):
                        shutil.copy2(src_path, dst_path)
                        successful_copies += 1
                    else:
                        print(f"File tidak ditemukan: {filename}")
                        failed_copies += 1
                elif is_pushdown == 1:
                    dst_path = os.path.join(pushdown_dir, filename)
                    if os.path.exists(src_path):
                        shutil.copy2(src_path, dst_path)
                        successful_copies += 1
                    else:
                        print(f"File tidak ditemukan: {filename}")
                        failed_copies += 1
            except Exception as e:
                print(f"Error saat memproses {filename}: {str(e)}")
                failed_copies += 1
                
        # Menghitung jumlah gambar di setiap folder
        pushup_count = len(os.listdir(pushup_dir))
        pushdown_count = len(os.listdir(pushdown_dir))
        
        print("\nProses selesai!")
        print(f"Jumlah gambar push-up: {pushup_count}")
        print(f"Jumlah gambar push-down: {pushdown_count}")
        print(f"Berhasil menyalin: {successful_copies} file")
        print(f"Gagal menyalin: {failed_copies} file")
        
    except Exception as e:
        print(f"Terjadi error: {str(e)}")
        # Menampilkan informasi lebih detail tentang error
        import traceback
        print("\nDetail error:")
        print(traceback.format_exc())

# Jalankan fungsi
if __name__ == "__main__":
    organize_pushup_images()