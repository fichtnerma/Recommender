import React from "react";
import RatingStars from "../Books/RatingStars";
import "./BookDetails.scss";
import { User } from "../../App";
import { Book, Rating } from "../../types/types";

interface BookDetailsProps {
	selectedBook: Book;
	onRate: (rating: number) => void;
	user?: User;
	userRating?: Rating;
}

export default function BookDetails({ selectedBook, user, onRate, userRating }: BookDetailsProps) {
	const { imageUrlLarge, author, rating_mean, rating_count, title, pubYear } = selectedBook;

	return (
		<div className="bookDetails">
			<div className={"imageWrapper"}>
				<img src={imageUrlLarge} alt={`The cover for the book „${title}“`}/>
				<RatingStars rating={+rating_mean}/>
				<span>{rating_count} {rating_count === 1 ? "Bewertung" : "Bewertungen"}</span>
			</div>

			<div className={"detailContent"}>
				<h2>{title}</h2>
				<h3>von {author}</h3>
				<h3>{pubYear}</h3>
				<p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt,
					atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem
					amet.
					Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae
					voluptatem amet. Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor
					explicabo possimus ipsam
					incidunt,
					atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae voluptatem
					amet.
					Quod. Lorem ipsum, dolor sit amet consectetur adipisicing elit. Iusto dolor explicabo possimus ipsam
					incidunt, atque error veritatis deleniti perferendis modi ea adipisci aut sit sint libero vitae
					voluptatem amet.
				</p>
			</div>

			{!!user ? <div className="ratingCTA">
				<h3>{userRating?.rating ? "Deine Bewertung" : "Jetzt bewerten"}</h3>
				<RatingStars user={user} rating={userRating?.rating ?? 0} canRate={true} onRate={onRate}/>
			</div> : null}
		</div>
	);
}
