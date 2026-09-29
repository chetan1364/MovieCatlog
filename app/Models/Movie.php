<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Movie extends Model
{
    use HasFactory;
    protected $fillable = ['title', 'release_year', 'duration_minutes', 'synopsis', 'poster_url', 'director_id'];

    public function director() {
        return $this->belongsTo(Director::class);
    }

    public function actors() {
        return $this->belongsToMany(Actor::class, 'movie_actors')->withPivot('character_name');
    }

    public function genres() {
        return $this->belongsToMany(Genre::class, 'movie_genres');
    }

    public function ratings() {
        return $this->hasMany(Rating::class);
    }
}
