<?php
	function makeTable($p){
	?>
		<table class="table table-responsive analytics-table">
			<thead>
			<tr>
				<th>Headline</th>
				<th>Links in Article</th>
				<th>Links per 1000 Words</th>
				<th>Link Quality</th>
				<th>Sources in Article</th>
				<th>Sources per 1000 Words</th>
				<th>Word Count</th>
			</tr>
			</thead>
			<tbody>
			<?php
			analyticsByHeadline($p);
			?>
			</tbody>
		</table>
	<?php }?>