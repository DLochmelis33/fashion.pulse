package cub.dlhf.fashionpulse

import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.FileProvider
import cub.dlhf.fashionpulse.theme.FashionPulseTheme
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.android.Android
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.request.forms.formData
import io.ktor.client.request.forms.submitFormWithBinaryData
import io.ktor.client.statement.bodyAsText
import io.ktor.http.Headers
import io.ktor.http.HttpHeaders
import io.ktor.http.isSuccess
import io.ktor.serialization.kotlinx.json.json
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.File

class MainActivity : ComponentActivity() {

    private val client = HttpClient(Android) {
        defaultRequest {
            url(BuildConfig.BACKEND_URL + "/analyze")
        }
        install(ContentNegotiation) {
            json()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            FashionPulseTheme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen()
                }
            }
        }
    }

    @Composable
    private fun MainScreen() {
        var takenPhotoUri: Uri? = null
        var userImageUri by remember { mutableStateOf<Uri?>(null) }
        var analysisState by remember { mutableStateOf<AnalysisStatus>(AnalysisStatus.Idle) }

        val pickImageLauncher = rememberLauncherForActivityResult(
            ActivityResultContracts.PickVisualMedia()
        ) {
            if (it != null) {
                userImageUri = it
                analysisState = AnalysisStatus.Idle
            }
        }
        val takePhotoLauncher = rememberLauncherForActivityResult(
            ActivityResultContracts.TakePicture()
        ) { ok ->
            if (ok) {
                userImageUri = takenPhotoUri
                analysisState = AnalysisStatus.Idle
            }
        }

        val coroutineScope = rememberCoroutineScope()

        fun handleError(userMessage: String, logMessage: String?) =
            coroutineScope.launch(Dispatchers.Main) {
                Log.e("fashion.pulse", logMessage ?: "<no message>")
                Toast.makeText(this@MainActivity, userMessage, Toast.LENGTH_LONG).show()
                analysisState = AnalysisStatus.Idle
            }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(20.dp),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            ImagePlaceholder(
                imageUri = userImageUri,
                modifier = Modifier
                    .heightIn(max = 400.dp)
                    .padding(20.dp)
            )
            ImagePicker(
                onTakePhoto = {
                    val tempFile = File.createTempFile("photo", ".jpg", cacheDir)
                    takenPhotoUri = FileProvider.getUriForFile(
                        this@MainActivity,
                        "$packageName.fileprovider",
                        tempFile
                    )
                    takePhotoLauncher.launch(takenPhotoUri)
                },
                onPickImage = {
                    pickImageLauncher.launch(
                        PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                    )
                },
                modifier = Modifier.padding(vertical = 5.dp)
            )
            AnalyzeButton(
                imageUri = userImageUri,
                analysisStatus = analysisState,
                onDisabledClick = {
                    Toast.makeText(
                        this@MainActivity,
                        "Select a new image to measure!",
                        Toast.LENGTH_SHORT
                    ).show()
                },
                onEnabledClick = { uri ->
                    coroutineScope.launch(Dispatchers.IO) {
                        val mediaType = contentResolver.getType(uri) ?: run {
                            handleError(
                                "Unsupported media type!",
                                "uri $uri has null media type"
                            )
                            return@launch
                        }
                        val imageBytes = contentResolver.openInputStream(uri)?.use {
                            it.readBytes()
                        } ?: run {
                            handleError(
                                "Cannot read your image :(",
                                "input stream for $uri is null"
                            )
                            return@launch
                        }
                        withContext(Dispatchers.Main) {
                            analysisState = AnalysisStatus.WaitingForResult
                        }
                        val response = client.submitFormWithBinaryData(formData = formData {
                            append("image", imageBytes, Headers.build {
                                append(HttpHeaders.ContentType, mediaType)
                                append(HttpHeaders.ContentDisposition, "filename=\"image.png\"")
                            })
                        })
                        if (!response.status.isSuccess()) {
                            handleError(
                                "Got an error from server :/",
                                "response code is not a success: ${response.status}\n${response.bodyAsText()}"
                            )
                            return@launch
                        }
                        val analysisResult = response.body<AnalysisStatus.ResultReady>()
                        withContext(Dispatchers.Main) {
                            analysisState = analysisResult
                        }
                    }
                },
                modifier = Modifier.padding(vertical = 5.dp)
            )
            (analysisState as? AnalysisStatus.ResultReady)?.let {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center,
                ) {
                    FashionResults(result = it)
                }
            }
        }
    }

}
