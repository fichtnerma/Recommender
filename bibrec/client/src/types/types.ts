export interface Book {
	isbn: string;
	isbn13: number;
	book_title: string;
	image_url_l: string;
	image_url_m: string;
	image_url_s: string;
	book_author: string;
	rating_count: number;
	rating_mean: number;
	year_of_publication: number;
	publisher: string;
}

export interface Rating {
	user_id: number,
	isbn: string,
	book_rating: number,
}
