<?php

namespace Proxy\Plugin;

use Proxy\Plugin\AbstractPlugin;
use Proxy\Event\ProxyEvent;

use Proxy\Html;

class XnxxPlugin extends AbstractPlugin {
	
	protected $url_pattern = 'xnxx.com';
	
	public function onCompleted(ProxyEvent $event){
		$response = $event['response'];
		
		$content = $response->getContent();
		
		$content = preg_replace_callback('/<img[^>]+src="([^"]+)"[^>]+data-src="([^"]+)/i', function($matches){
			return str_replace($matches[1], $matches[2], $matches[0]);
		}, $content);
		
		if(preg_match('/VideoUrlHigh\(\'([^\']+)/', $content, $matches)){
			$url = $matches[1];
			
			$player = vid_player($url, 938, 476);
			
			$content = Html::replace_inner('#video-player-bg', $player, $content);
		}
		
		// too many ads
		$content = Html::remove_scripts($content);
		$response->setContent($content);
	}
	
}