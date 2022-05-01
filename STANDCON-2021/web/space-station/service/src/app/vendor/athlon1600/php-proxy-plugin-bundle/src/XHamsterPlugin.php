<?php

namespace Proxy\Plugin;

use Proxy\Plugin\AbstractPlugin;
use Proxy\Event\ProxyEvent;
use Proxy\Html;

class XHamsterPlugin extends AbstractPlugin {

	protected $url_pattern = 'xhamster.com';
	
	public function onBeforeRequest(ProxyEvent $event){
		// we do not want to force mobile this time
		$event['request']->headers->set('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0');
	}
	
	private function find_video($html){
		$file = false;
		
		if(preg_match('/mp4File":"([^"]+)/', $html, $matches)){
			$file = $matches[1];
			return stripslashes($file);
		}
		
		return $file;
	}
	
	public function onCompleted(ProxyEvent $event){
		$response = $event['response'];
		$content = $response->getContent();
		
		// remove ads
		$content = HTML::remove('.ts', $content);
		
		// is this video page?
		$file = $this->find_video($content);
		if($file){
			$player = vid_player($file, 950, 650);
			$player = str_replace('<video', '<video style="display:block;', $player);
			
			//$content = HTML::replace_inner('#video_box', $player, $content);
			$content = HTML::replace_inner('#player-container', $player, $content);
			
			// remove "show comments" button
			$content = HTML::remove('#commentToggle', $content);
			
			// display all comments by default
			$content = str_replace('<div class="comments_block"', '<div style="display:block;" class="comments_block"', $content);
		}
		
		$content = Html::remove_scripts($content);
		
		$response->setContent($content);
	}
}

?>