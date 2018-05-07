using System.Net;
using System;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Primitives;

public static async Task<IActionResult> Run(HttpRequest req, TraceWriter log) {

   Stream image = req.Body;
   dynamic message = req.Query;

    // If Scott is here
     if((string)message["class"] == "Scott" && double.Parse(message["confidence"]) > 0.5) 
    {
      // Call a logic app to post a tweet
      await client.PostAsync(Environment.GetEnvironmentVariable("LOGIC_APP_URL"), new StreamContent(image));
    
      await FlashLights(1);
    }

     else if((string)message["class"] == "NotScott" && double.Parse(message["confidence"]) > 0.5) 
    {
      await FlashLights(0);
    }

    return new OkResult();
}

private static HttpClient client = new HttpClient();

public static async Task FlashLights(int type)
{
    string urlpath = type == 1 ? "yes" : "no";
    var addresslist = Dns.GetHostAddresses("StartupContainer");
    await client.PostAsJsonAsync<double>("http://" + addresslist[0].ToString() + ":8082/" + urlpath, 1);     
}