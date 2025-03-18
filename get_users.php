<?php
// Указываем путь к файлу базы данных SQLite
$dbFile = 'C:\Users\Ut\DisukoTown\db\db';  // Путь к файлу базы данных SQLite

try {
    // Устанавливаем соединение с базой данных SQLite
    $db = new PDO('sqlite:' . $dbFile);

    // Включаем режим исключения ошибок для отладки
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Выполнение SQL-запроса для получения данных
    $stmt = $db->query('SELECT * FROM Users');

    // Получение результатов в виде ассоциативного массива
    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Преобразование данных в JSON-формат
    echo json_encode($results);
} catch(PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>