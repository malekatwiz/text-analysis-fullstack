using Jobs.Api;
using System.Text.Json.Serialization;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddScoped<JobPostingsService>();

builder.Services.AddCors(builder =>
{
    builder.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();
app.UseCors();

app.MapPost("/jobs/postings", async (JobPosting jobPosting) =>
{
    if (string.IsNullOrWhiteSpace(jobPosting.SourceLink) || string.IsNullOrWhiteSpace(jobPosting.Description))
    {
        return Results.BadRequest("Source link and description are required.");
    }

    var cleanedDescription = jobPosting.Description.Trim();
    cleanedDescription = cleanedDescription.Replace("\r\n", " ").Replace("\n", " ");
    cleanedDescription = cleanedDescription.Replace("\r", " ").Replace("\t", " ");

    if (string.IsNullOrWhiteSpace(cleanedDescription))
    {
         return Results.BadRequest("Description cannot be empty after cleaning.");
    }

    jobPosting.Description = cleanedDescription;

    var jobPostingService = app.Services.GetService<JobPostingsService>() 
        ?? throw new InvalidOperationException("JobPostingsService is not registered.");

    await jobPostingService.CreateJobPostingAsync(jobPosting);
    return Results.Accepted();
})
    .WithName("PostJobPosting")
    .WithOpenApi();

await app.RunAsync();

public record JobPosting
{
    [JsonPropertyName("source_link")]
    public string SourceLink { get; set; }

    [JsonPropertyName("description")]
    public string Description { get; set; }
}
