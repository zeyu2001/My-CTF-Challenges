<!DOCTYPE html>
<html>
<?php include "includes/head.php" ?>

<body>
<?php include "includes/nav.php" ?>

<div class="jumbotron landing-head bg-primary text-white">
	<h1 class="display-4 landing-title" align="center">Space Station</h1>
	<p class="lead" align="center">Where do you want to go?</p>
	<div class="landing-img"></div>
</div>

<div id="container" class="container">

	<?php if(isset($error_msg)){ ?>
	
	<div id="error">
		<p><?php echo strip_tags($error_msg); ?></p>
	</div>
	
	<?php } ?>
	
	<div id="frm" class="text-center">
	
	<!-- I wouldn't touch this part -->
	
		<form action="index.php" method="post" style="margin-bottom:0;">
			<input name="url" type="text" style="width:400px;" autocomplete="off" placeholder="http://" />
			<input type="submit" value="Go" />
		</form>
		
		<script type="text/javascript">
			document.getElementsByName("url")[0].focus();
		</script>
		
	<!-- [END] -->
	
	</div>
	
</div>

<div id="footer" class="page-footer text-center container">
	Powered by <a href="//www.php-proxy.com/" target="_blank">PHP-Proxy</a>
</div>

</body>
</html>