const newWorkbook = XLSX.utils.book_new();
        let processedData = [];

        // Process each row
        for (let row of rows_to_proceed) {
            // Convert row to desired format
            const formattedRow = {
                izlenecekKelime: row['İzlenecek Kelime'],
                markaAdi: row['Marka Adı'],
                firma: row['Firma'],
                basvuruNo: row['Başvuru No'],
                sinif: row['Sınıf'],
                benzerlik: row['Benzerlik']
            };

            // Check first brand
            if (formattedRow.izlenecekKelime === formattedRow.markaAdi) {
                formattedRow.backgroundColor = '#E3F2FD';  // Light blue
                formattedRow.isFirstBrand = true;
            }

            processedData.push(formattedRow);
        }

        // Convert processed data to worksheet
        const ws = XLSX.utils.json_to_sheet(processedData);

        // Add the worksheet to workbook
        XLSX.utils.book_append_sheet(newWorkbook, ws, 'Processed Data');