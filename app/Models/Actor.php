<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Actor extends Model
{
    use HasFactory;
    protected $fillable = ['name', 'bio'];

    public function movies() {
        return $this->belongsToMany(Movie::class, 'movie_actors')->withPivot('character_name');
    }
}
