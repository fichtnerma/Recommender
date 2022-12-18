import loadingCircle from "../../assets/oval.svg";
import React from "react";

export default function LoadingIndicator() {
	return <div className={"loadingIndicator"}>
		<img src={loadingCircle} alt={"A spinning circle to indicate loading content"}/>
		<span>Lade Bücher...</span>
	</div>;
}
