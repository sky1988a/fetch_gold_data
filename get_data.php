<?php
// 连接数据库
$conn = new PDO('sqlite:gold_prices.db');

// 查询数据
$query = "SELECT date, price FROM gold_prices";
$stmt = $conn->query($query);
$data = $stmt->fetchAll(PDO::FETCH_ASSOC);

// 返回JSON数据
header('Content-Type: application/json');
echo json_encode($data);
?>