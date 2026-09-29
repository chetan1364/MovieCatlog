<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return file_get_contents(public_path('index.html'));
});

Route::get('/movie', function () {
    return file_get_contents(public_path('movie.html'));
});

Route::get('/admin', function (\Illuminate\Http\Request $request) {
    if ($request->getUser() !== 'admin' || $request->getPassword() !== 'password') {
        $headers = ['WWW-Authenticate' => 'Basic realm="Admin Panel"'];
        return response('Unauthorized', 401, $headers);
    }
    return file_get_contents(public_path('admin.html'));
});
