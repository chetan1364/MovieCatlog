<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Rating extends Model
{
    use HasFactory;
    protected $fillable = ['movie_id', 'user_name', 'score', 'review'];

    public function movie() {
        return $this->belongsTo(Movie::class);
    }
}
