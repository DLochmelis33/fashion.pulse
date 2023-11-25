package cub.dlhf.fashionpulse

import android.net.Uri
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.IntrinsicSize
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage

@Composable
fun ImagePicker(
    takePhotoCallback: () -> Unit,
    pickImageCallback: () -> Unit,
) {
    Row(
        horizontalArrangement = Arrangement.SpaceEvenly,
        modifier = Modifier
            .height(IntrinsicSize.Max)
    ) {
        Button(
            onClick = { takePhotoCallback() }, modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            Text(text = "Take a photo", textAlign = TextAlign.Center)
        }
        Spacer(modifier = Modifier.width(3.dp))
        Button(
            onClick = { pickImageCallback() }, modifier = Modifier
                .fillMaxSize()
                .weight(1f)
        ) {
            Text(text = "Pick from gallery", textAlign = TextAlign.Center)
        }
    }
}

@Composable
fun ImagePlaceholder(
    imageUri: Uri?,
    modifier: Modifier = Modifier,
) {
    Box(
        modifier = modifier
            .fillMaxSize()
            .clip(RoundedCornerShape(10.dp)),
        contentAlignment = Alignment.Center,
    ) {
        if (imageUri == null) {
            Surface(
                modifier = Modifier.fillMaxSize(),
                color = MaterialTheme.colorScheme.secondaryContainer
            ) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "Pick an image to analyze",
                        style = MaterialTheme.typography.labelSmall,
                    )
                }
            }
        } else {
            Box(modifier = Modifier.clip(RoundedCornerShape(10.dp))) {
                AsyncImage(model = imageUri.toString(), contentDescription = "chosen image")
            }
        }
    }
}
