import React, { useEffect, useState } from "react";
import "./Rating.scss";
import { User } from "../../App";

type RatingProps = {
	user?: User;
	rating: number;
	canRate?: false;
	onRate?: (rating: number) => void;
} | {
	user?: User;
	rating: number;
	canRate: true;
	onRate: (rating: number) => void;
}

export default function RatingStars({ rating, canRate, user, onRate }: RatingProps) {
	const maxRating = 10;
	const [currentRating, setCurrentRating] = useState(rating || 0);

	useEffect(() => {
		setCurrentRating(rating);
	}, [rating]);

	const calculatedWidth = `${(1 - currentRating / maxRating) * 100}%`;

	return (
		<div className="rating">
			<div className={`stars ${canRate ? "cursorPointer" : ""}`}>
				{[...Array(maxRating)].map((x, i) => (
					<svg viewBox="0 0 576 512" width="100" key={i + 1} onClick={() => {
						if (!canRate || !user) return;
						const selectedRating = i + 1;
						onRate && onRate(selectedRating);
						setCurrentRating(selectedRating);
					}}>
						<path
							d="M259.3 17.8L194 150.2 47.9 171.5c-26.2 3.8-36.7 36.1-17.7 54.6l105.7 103-25 145.5c-4.5 26.3 23.2 46 46.4 33.7L288 439.6l130.7 68.7c23.2 12.2 50.9-7.4 46.4-33.7l-25-145.5 105.7-103c19-18.5 8.5-50.8-17.7-54.6L382 150.2 316.7 17.8c-11.7-23.6-45.6-23.9-57.4 0z"/>
					</svg>
				))}

				<div style={{
					width: calculatedWidth,
					pointerEvents: "none"
				}} className="cover"/>
			</div>
		</div>
	);
}
