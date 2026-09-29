<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Models\Movie;
use App\Models\Director;
use App\Models\Actor;
use App\Models\Genre;
use App\Models\Rating;

Route::get('/movies', function (Request $request) {
    $query = Movie::with(['director', 'actors', 'genres']);

    if ($request->has('search') && $request->search != '') {
        $search = $request->search;
        $query->where(function($q) use ($search) {
            $q->where('title', 'like', "%{$search}%")
              ->orWhereHas('director', function($q) use ($search) {
                  $q->where('name', 'like', "%{$search}%");
              })
              ->orWhereHas('actors', function($q) use ($search) {
                  $q->where('name', 'like', "%{$search}%");
              });
        });
    }

    if ($request->has('genre') && $request->genre != '') {
        $genre = $request->genre;
        $query->whereHas('genres', function($q) use ($genre) {
            $q->where('name', $genre);
        });
    }

    if ($request->has('year_from') && $request->year_from != '') {
        $query->where('release_year', '>=', $request->year_from);
    }
    
    if ($request->has('year_to') && $request->year_to != '') {
        $query->where('release_year', '<=', $request->year_to);
    }

    $sortBy = $request->input('sort_by', 'title');
    $sortOrder = $request->input('sort_order', 'asc');
    
    if ($sortBy === 'avg_rating') {
        $query->withAvg('ratings as avg_rating', 'score')->orderBy('avg_rating', $sortOrder);
    } else {
        $query->orderBy($sortBy, $sortOrder);
    }

    $movies = $query->get();

    return response()->json([
        'success' => true,
        'data' => $movies,
        'count' => $movies->count()
    ]);
});

Route::get('/movies/{id}', function ($id) {
    $movie = Movie::with(['director', 'actors', 'genres', 'ratings'])->find($id);
    if (!$movie) return response()->json(['success' => false, 'error' => 'Movie not found'], 404);
    
    return response()->json(['success' => true, 'data' => $movie]);
});

Route::get('/directors', function () {
    $directors = Director::all();
    return response()->json(['success' => true, 'data' => $directors, 'count' => $directors->count()]);
});

Route::get('/directors/{id}', function ($id) {
    $director = Director::with('movies')->find($id);
    if (!$director) return response()->json(['success' => false, 'error' => 'Not found'], 404);
    return response()->json(['success' => true, 'data' => $director]);
});

Route::get('/actors', function () {
    $actors = Actor::all();
    return response()->json(['success' => true, 'data' => $actors, 'count' => $actors->count()]);
});

Route::get('/actors/{id}', function ($id) {
    $actor = Actor::with('movies')->find($id);
    if (!$actor) return response()->json(['success' => false, 'error' => 'Not found'], 404);
    return response()->json(['success' => true, 'data' => $actor]);
});

Route::get('/genres', function () {
    $genres = Genre::all();
    return response()->json(['success' => true, 'data' => $genres, 'count' => $genres->count()]);
});

Route::get('/genres/{id}', function ($id) {
    $genre = Genre::with('movies')->find($id);
    if (!$genre) return response()->json(['success' => false, 'error' => 'Not found'], 404);
    return response()->json(['success' => true, 'data' => $genre]);
});
