<!DOCTYPE html>
<html lang="en">
<head>
	<title>Security Logs</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->	
	<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
</head>
<body>

	<header>
		<div>
			<h1 class="title">Smart Door Lock Security Logs</h1>
		</div>
	</header>

	<div class="limiter">
		<div class="container-table100">
			<div class="wrap-table100">
				<div class="table100 ver5 m-b-110">
					<div class="table100-head">
						<table>
							<thead>
								<tr class="row100 head">
									<th class="cell100 column1">ID</th>
									<th class="cell100 column2">Log Report</th>
									<th class="cell100 column3">Time Stamp</th>
								</tr>
							</thead>
						</table>
					</div>

					<div class="table100-body js-pscroll">
						<table>
							<tbody>

								<!-- <tr class="row100 body">
									<td class="cell100 column1">1</td>
									<td class="cell100 column2">Face Recognized, Door Unlocked</td>
									<td class="cell100 column3">'01/15/2022, 11:44:39'</td>
									
								</tr> -->
								
								<?php
                                    $conn = mysqli_connect("cypherdb.cl6emmhgfani.ap-southeast-1.rds.amazonaws.com","admin","cypherpervasive","cypher");
                                    if($conn->connect_error){
                                        die("Connection failed:".$conn->connect_error);
                                    }

                                    $sql  = "SELECT * from logs";
                                    $result = $conn->query($sql);

									if($result-> num_rows>0){
										while($row = $result->fetch_assoc()){
											echo "<tr><td class='cell100 column1'>".$row["id"]."</td><td>".$row["status"]."</td><td>".$row["datetime"]."</td></tr>";
										}
										echo"</table>";
									}
									else{
										echo "0 Result";
									}
									$conn->close();
                                ?>
			

							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>


<!--===============================================================================================-->	
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/perfect-scrollbar/perfect-scrollbar.min.js"></script>
	<script>
		$('.js-pscroll').each(function(){
			var ps = new PerfectScrollbar(this);

			$(window).on('resize', function(){
				ps.update();
			})
		});
			
		
	</script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

</body>
</html>