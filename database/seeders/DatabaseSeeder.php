<?php

namespace Database\Seeders;

use App\Models\Actor;
use App\Models\Director;
use App\Models\Genre;
use App\Models\Movie;
use App\Models\Rating;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $genres = ['Action', 'Drama', 'Romance', 'Comedy', 'Thriller', 'Sci-Fi', 'Masala', 'Family', 'Historical'];
        $genreModels = [];
        foreach ($genres as $genreName) {
            $genreModels[$genreName] = Genre::create(['name' => $genreName]);
        }

        $directorsData = [
            ['name' => 'Sukumar', 'bio' => 'A prominent director in Telugu cinema.', 'birth_year' => 1970],
            ['name' => 'Trivikram Srinivas', 'bio' => 'Known as the Guruji of Telugu cinema.', 'birth_year' => 1971],
            ['name' => 'S. S. Rajamouli', 'bio' => 'Visionary director behind Baahubali and RRR.', 'birth_year' => 1973],
            ['name' => 'Sandeep Reddy Vanga', 'bio' => 'Known for bold films.', 'birth_year' => 1981],
            ['name' => 'Atlee', 'bio' => 'Successful director in Tamil cinema.', 'birth_year' => 1992],
            ['name' => 'Prashanth Neel', 'bio' => 'Creator of the KGF universe.', 'birth_year' => 1980],
            ['name' => 'Nitesh Tiwari', 'bio' => 'Director of Dangal.', 'birth_year' => 1973],
            ['name' => 'Rajkumar Hirani', 'bio' => 'Director of PK.', 'birth_year' => 1962],
            ['name' => 'Surender Reddy', 'bio' => 'Telugu director.', 'birth_year' => 1975],
            ['name' => 'V. V. Vinayak', 'bio' => 'Telugu mass director.', 'birth_year' => 1974],
            ['name' => 'Boyapati Srinu', 'bio' => 'Mass action director.', 'birth_year' => 1971],
            ['name' => 'Harish Shankar', 'bio' => 'Telugu director.', 'birth_year' => 1979],
            ['name' => 'Lokesh Kanagaraj', 'bio' => 'LCU creator.', 'birth_year' => 1986],
            ['name' => 'Rishab Shetty', 'bio' => 'Director and actor.', 'birth_year' => 1983],
            ['name' => 'Siddharth Anand', 'bio' => 'Bollywood action director.', 'birth_year' => 1978],
            ['name' => 'Christopher Nolan', 'bio' => 'Visionary British-American director.', 'birth_year' => 1970],
            ['name' => 'James Cameron', 'bio' => 'Canadian filmmaker.', 'birth_year' => 1954],
        ];
        
        $directors = [];
        foreach ($directorsData as $dir) {
            $directors[$dir['name']] = Director::create($dir);
        }

        $actorsData = [
            ['name' => 'Allu Arjun', 'bio' => 'Icon Star of Telugu Cinema.'],
            ['name' => 'Ram Charan', 'bio' => 'Global Star.'],
            ['name' => 'Prabhas', 'bio' => 'Rebel Star.'],
            ['name' => 'Shah Rukh Khan', 'bio' => 'King Khan.'],
            ['name' => 'Thalapathy Vijay', 'bio' => 'Leading star of Tamil cinema.'],
            ['name' => 'Rashmika Mandanna', 'bio' => 'National Crush.'],
            ['name' => 'Pooja Hegde', 'bio' => 'Popular actress.'],
            ['name' => 'Yash', 'bio' => 'Rocking Star.'],
            ['name' => 'Aamir Khan', 'bio' => 'Mr. Perfectionist.'],
            ['name' => 'Ranbir Kapoor', 'bio' => 'Bollywood star.'],
            ['name' => 'Shahid Kapoor', 'bio' => 'Bollywood star.'],
            ['name' => 'Kamal Haasan', 'bio' => 'Ulaganayagan.'],
            ['name' => 'Rishab Shetty', 'bio' => 'Kannada star.'],
            ['name' => 'Shruti Haasan', 'bio' => 'Actress.'],
            ['name' => 'Rakul Preet Singh', 'bio' => 'Actress.'],
            ['name' => 'Leonardo DiCaprio', 'bio' => 'Academy Award-winning actor.'],
            ['name' => 'Christian Bale', 'bio' => 'Known for versatile roles.'],
            ['name' => 'Sam Worthington', 'bio' => 'Australian actor.'],
            ['name' => 'Zoe Saldana', 'bio' => 'American actress.'],
            ['name' => 'Cillian Murphy', 'bio' => 'Irish actor.'],
        ];

        $actors = [];
        foreach ($actorsData as $act) {
            $actors[$act['name']] = Actor::create($act);
        }

        $moviesData = [
            [
                'title' => 'Pushpa: The Rise', 'release_year' => 2021, 'duration_minutes' => 179,
                'synopsis' => 'A laborer rises through the ranks of a smuggling syndicate.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/7/75/Pushpa_-_The_Rise_%282021_film%29.jpg',
                'director' => 'Sukumar', 'actors' => ['Allu Arjun', 'Rashmika Mandanna'], 'genres' => ['Action', 'Drama', 'Thriller', 'Masala']
            ],
            [
                'title' => 'Ala Vaikunthapurramuloo', 'release_year' => 2020, 'duration_minutes' => 165,
                'synopsis' => 'Swapped at birth, a man grows up in a middle-class family.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/2/28/Ala_Vaikunthapurramuloo.jpeg',
                'director' => 'Trivikram Srinivas', 'actors' => ['Allu Arjun', 'Pooja Hegde'], 'genres' => ['Action', 'Drama', 'Family', 'Comedy']
            ],
            [
                'title' => 'Arya', 'release_year' => 2004, 'duration_minutes' => 150,
                'synopsis' => 'A free-spirited guy falls in love.',
                'poster_url' => 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQDs9EbfiKFsLjAtubAcHAdssty_vQYkdtbCoj5WlKfw&s=10',
                'director' => 'Sukumar', 'actors' => ['Allu Arjun'], 'genres' => ['Romance', 'Action']
            ],
            [
                'title' => 'Julayi', 'release_year' => 2012, 'duration_minutes' => 160,
                'synopsis' => 'A witty young man gets involved in a bank robbery.',
                'poster_url' => 'https://m.media-amazon.com/images/S/pv-target-images/1ebd4534263352328649384bb1c6428f1809692c55f3facea022fece648d5ded.jpg',
                'director' => 'Trivikram Srinivas', 'actors' => ['Allu Arjun'], 'genres' => ['Action', 'Comedy']
            ],
            [
                'title' => 'Race Gurram', 'release_year' => 2014, 'duration_minutes' => 163,
                'synopsis' => 'Two brothers with opposite mindsets clash with a politician.',
                'poster_url' => 'https://jiotvimages.cdn.jio.com/imagespublic/76/52/45b90bea24045e13a37f4ec836b412e3_1703282750687_l_medium.jpg',
                'director' => 'Surender Reddy', 'actors' => ['Allu Arjun', 'Shruti Haasan'], 'genres' => ['Action', 'Comedy']
            ],
            [
                'title' => 'S/O Satyamurthy', 'release_year' => 2015, 'duration_minutes' => 162,
                'synopsis' => 'A son tries to uphold his deceased father\'s values.',
                'poster_url' => 'https://sund-images.sunnxt.com/7346/1000x1500_0b1735ff-6ff9-4f7c-b089-7f21f0f97db9.jpg',
                'director' => 'Trivikram Srinivas', 'actors' => ['Allu Arjun'], 'genres' => ['Drama', 'Family']
            ],
            [
                'title' => 'Badrinath', 'release_year' => 2011, 'duration_minutes' => 140,
                'synopsis' => 'A protector of a temple falls in love.',
                'poster_url' => 'https://m.media-amazon.com/images/S/pv-target-images/4fa292762965c82fbb542bafe6d2272c3adf64a21c314c2f7aa08136dfb48670.jpg',
                'director' => 'V. V. Vinayak', 'actors' => ['Allu Arjun'], 'genres' => ['Action', 'Romance']
            ],
            [
                'title' => 'Desamuduru', 'release_year' => 2007, 'duration_minutes' => 150,
                'synopsis' => 'A reporter falls for a sanyasin.',
                'poster_url' => 'https://static.toiimg.com/photo/61338976.cms',
                'director' => 'Boyapati Srinu', 'actors' => ['Allu Arjun'], 'genres' => ['Action', 'Romance']
            ],
            [
                'title' => 'Sarrainodu', 'release_year' => 2016, 'duration_minutes' => 159,
                'synopsis' => 'An intense young man fights against a corrupt politician.',
                'poster_url' => 'https://m.media-amazon.com/images/M/MV5BYWQ1MzhlYjUtMmE1NS00ZWY4LWI1ZDgtMThmOWJhZGU4Mzk5XkEyXkFqcGc@._V1_.jpg',
                'director' => 'Boyapati Srinu', 'actors' => ['Allu Arjun', 'Rakul Preet Singh'], 'genres' => ['Action', 'Masala']
            ],
            [
                'title' => 'DJ: Duvvada Jagannadham', 'release_year' => 2017, 'duration_minutes' => 152,
                'synopsis' => 'A Brahmin cook turns into a vigilante.',
                'poster_url' => 'https://c.saavncdn.com/161/DJ-Duvvada-Jagannadham-Telugu-2017-500x500.jpg',
                'director' => 'Harish Shankar', 'actors' => ['Allu Arjun', 'Pooja Hegde'], 'genres' => ['Action', 'Comedy']
            ],
            [
                'title' => 'RRR', 'release_year' => 2022, 'duration_minutes' => 187,
                'synopsis' => 'Two legendary revolutionaries journey away from home.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/d/d7/RRR_Poster.jpg',
                'director' => 'S. S. Rajamouli', 'actors' => ['Ram Charan'], 'genres' => ['Action', 'Drama', 'Masala', 'Historical']
            ],
            [
                'title' => 'Jawan', 'release_year' => 2023, 'duration_minutes' => 169,
                'synopsis' => 'A high-octane action thriller.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/3/39/Jawan_film_poster.jpg',
                'director' => 'Atlee', 'actors' => ['Shah Rukh Khan', 'Thalapathy Vijay'], 'genres' => ['Action', 'Thriller']
            ],
            [
                'title' => 'Pathaan', 'release_year' => 2023, 'duration_minutes' => 146,
                'synopsis' => 'An Indian spy takes on the leader of a group of mercenaries.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/c/c3/Pathaan_film_poster.jpg',
                'director' => 'Siddharth Anand', 'actors' => ['Shah Rukh Khan'], 'genres' => ['Action', 'Thriller']
            ],
            [
                'title' => 'KGF: Chapter 1', 'release_year' => 2018, 'duration_minutes' => 155,
                'synopsis' => 'A young man seeks power and wealth.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/c/cc/K.G.F_Chapter_1_poster.jpg',
                'director' => 'Prashanth Neel', 'actors' => ['Yash'], 'genres' => ['Action', 'Drama']
            ],
            [
                'title' => 'KGF: Chapter 2', 'release_year' => 2022, 'duration_minutes' => 168,
                'synopsis' => 'Rocky establishes himself as the kingpin of KGF.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/d/d0/K.G.F_Chapter_2.jpg',
                'director' => 'Prashanth Neel', 'actors' => ['Yash'], 'genres' => ['Action', 'Drama']
            ],
            [
                'title' => 'Baahubali: The Beginning', 'release_year' => 2015, 'duration_minutes' => 159,
                'synopsis' => 'A young man learns about his royal heritage.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/5/5f/Baahubali_The_Beginning_poster.jpg',
                'director' => 'S. S. Rajamouli', 'actors' => ['Prabhas'], 'genres' => ['Action', 'Drama', 'Historical']
            ],
            [
                'title' => 'Baahubali 2: The Conclusion', 'release_year' => 2017, 'duration_minutes' => 167,
                'synopsis' => 'Amarendra Baahubali\'s story.',
                'poster_url' => 'https://m.media-amazon.com/images/I/71i8a-PnChL._AC_UF350,350_QL80_.jpg',
                'director' => 'S. S. Rajamouli', 'actors' => ['Prabhas'], 'genres' => ['Action', 'Drama', 'Historical']
            ],
            [
                'title' => 'Dangal', 'release_year' => 2016, 'duration_minutes' => 161,
                'synopsis' => 'Former wrestler trains his daughters.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/9/99/Dangal_Poster.jpg',
                'director' => 'Nitesh Tiwari', 'actors' => ['Aamir Khan'], 'genres' => ['Drama', 'Family']
            ],
            [
                'title' => 'PK', 'release_year' => 2014, 'duration_minutes' => 153,
                'synopsis' => 'An alien lands on Earth and asks questions.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/c/c3/PK_poster.jpg',
                'director' => 'Rajkumar Hirani', 'actors' => ['Aamir Khan'], 'genres' => ['Comedy', 'Drama', 'Sci-Fi']
            ],
            [
                'title' => 'Animal', 'release_year' => 2023, 'duration_minutes' => 201,
                'synopsis' => 'A son\'s obsessive love for his father.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/9/90/Animal_%282023_film%29_poster.jpg',
                'director' => 'Sandeep Reddy Vanga', 'actors' => ['Ranbir Kapoor', 'Rashmika Mandanna'], 'genres' => ['Action', 'Drama', 'Thriller']
            ],
            [
                'title' => 'Kabir Singh', 'release_year' => 2019, 'duration_minutes' => 172,
                'synopsis' => 'A surgeon goes on a self-destructive path.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/d/dc/Kabir_Singh.jpg',
                'director' => 'Sandeep Reddy Vanga', 'actors' => ['Shahid Kapoor'], 'genres' => ['Drama', 'Romance']
            ],
            [
                'title' => 'Leo', 'release_year' => 2023, 'duration_minutes' => 164,
                'synopsis' => 'A cafe owner gets involved in a drug cartel.',
                'poster_url' => '/posters/leo.jpg',
                'director' => 'Lokesh Kanagaraj', 'actors' => ['Thalapathy Vijay'], 'genres' => ['Action', 'Thriller']
            ],
            [
                'title' => 'Master', 'release_year' => 2021, 'duration_minutes' => 179,
                'synopsis' => 'An alcoholic professor is sent to a juvenile school.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/5/53/Master_2021_poster.jpg',
                'director' => 'Lokesh Kanagaraj', 'actors' => ['Thalapathy Vijay'], 'genres' => ['Action', 'Thriller']
            ],
            [
                'title' => 'Vikram', 'release_year' => 2022, 'duration_minutes' => 173,
                'synopsis' => 'A special investigator uncovers a drug syndicate.',
                'poster_url' => 'https://m.media-amazon.com/images/M/MV5BNDEyMWQ0ZDktNTY0MC00YWRkLWFlMjQtMDUxMjRlMDhmMmRlXkEyXkFqcGc@._V1_.jpg',
                'director' => 'Lokesh Kanagaraj', 'actors' => ['Kamal Haasan'], 'genres' => ['Action', 'Thriller']
            ],
            [
                'title' => 'Kantara', 'release_year' => 2022, 'duration_minutes' => 148,
                'synopsis' => 'A conflict between nature and humans.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/8/84/Kantara_poster.jpeg',
                'director' => 'Rishab Shetty', 'actors' => ['Rishab Shetty'], 'genres' => ['Action', 'Thriller', 'Drama']
            ],
            [
                'title' => 'Inception', 'release_year' => 2010, 'duration_minutes' => 148,
                'synopsis' => 'A thief who steals corporate secrets through the use of dream-sharing technology.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg',
                'director' => 'Christopher Nolan', 'actors' => ['Leonardo DiCaprio'], 'genres' => ['Action', 'Sci-Fi', 'Thriller']
            ],
            [
                'title' => 'The Dark Knight', 'release_year' => 2008, 'duration_minutes' => 152,
                'synopsis' => 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg',
                'director' => 'Christopher Nolan', 'actors' => ['Christian Bale'], 'genres' => ['Action', 'Drama', 'Thriller']
            ],
            [
                'title' => 'Avatar', 'release_year' => 2009, 'duration_minutes' => 162,
                'synopsis' => 'A paraplegic Marine dispatched to the moon Pandora on a unique mission.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/d/d6/Avatar_%282009_film%29_poster.jpg',
                'director' => 'James Cameron', 'actors' => ['Sam Worthington', 'Zoe Saldana'], 'genres' => ['Action', 'Sci-Fi']
            ],
            [
                'title' => 'Avatar: The Way of Water', 'release_year' => 2022, 'duration_minutes' => 192,
                'synopsis' => 'Jake Sully lives with his newfound family formed on the extrasolar moon Pandora.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/5/54/Avatar_The_Way_of_Water_poster.jpg',
                'director' => 'James Cameron', 'actors' => ['Sam Worthington', 'Zoe Saldana'], 'genres' => ['Action', 'Sci-Fi']
            ],
            [
                'title' => 'Oppenheimer', 'release_year' => 2023, 'duration_minutes' => 180,
                'synopsis' => 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg',
                'director' => 'Christopher Nolan', 'actors' => ['Cillian Murphy'], 'genres' => ['Drama', 'Historical']
            ],
            [
                'title' => 'Interstellar', 'release_year' => 2014, 'duration_minutes' => 169,
                'synopsis' => 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'poster_url' => 'https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg',
                'director' => 'Christopher Nolan', 'actors' => ['Leonardo DiCaprio'], 'genres' => ['Drama', 'Sci-Fi']
            ],
        ];

        foreach ($moviesData as $data) {
            $movie = Movie::create([
                'title' => $data['title'],
                'release_year' => $data['release_year'],
                'duration_minutes' => $data['duration_minutes'],
                'synopsis' => $data['synopsis'],
                'poster_url' => $data['poster_url'],
                'director_id' => $directors[$data['director']]->id
            ]);

            foreach ($data['actors'] as $actorName) {
                $movie->actors()->attach($actors[$actorName]->id, ['character_name' => 'Lead Role']);
            }

            foreach ($data['genres'] as $genreName) {
                $movie->genres()->attach($genreModels[$genreName]->id);
            }
            
            $reviewCount = rand(20, 60);
            for ($i = 0; $i < $reviewCount; $i++) {
                Rating::create([
                    'movie_id' => $movie->id,
                    'user_name' => 'User' . rand(1000, 9999),
                    'score' => rand(7, 10),
                    'review' => 'Great movie!',
                ]);
            }
        }
    }
}
