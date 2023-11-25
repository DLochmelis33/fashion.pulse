package cub.dlhf.fashionpulse

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.core.content.FileProvider
import cub.dlhf.fashionpulse.theme.FashionPulseTheme
import java.io.File

class MainActivity : ComponentActivity() {

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
    fun MainScreen() {
        var takenPhotoUri: Uri? = null
        var userImageUri by remember { mutableStateOf<Uri?>(null) }

        val pickImageLauncher = rememberLauncherForActivityResult(
            ActivityResultContracts.PickVisualMedia()
        ) {
            userImageUri = it
        }
        val takePhotoLauncher = rememberLauncherForActivityResult(
            ActivityResultContracts.TakePicture()
        ) { ok ->
            if (ok) {
                userImageUri = takenPhotoUri
            }
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(50.dp),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            ImagePlaceholder(imageUri = userImageUri, modifier = Modifier.heightIn(max = 400.dp))
            Spacer(modifier = Modifier.height(10.dp))
            ImagePicker(
                takePhotoCallback = {
                    val tempFile = File.createTempFile("photo", ".jpg", cacheDir)
                    takenPhotoUri = FileProvider.getUriForFile(
                        this@MainActivity,
                        "$packageName.fileprovider",
                        tempFile
                    )
                    takePhotoLauncher.launch(takenPhotoUri)
                },
                pickImageCallback = {
                    pickImageLauncher.launch(
                        PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly)
                    )
                }
            )

        }
    }
}
